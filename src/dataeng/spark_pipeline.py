from __future__ import annotations
import os
from typing import Optional

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F


def build_spark_session(app_name: str = "engagement_etl", master: str = "local[*]") -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.ui.enabled", "false")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )


def load_raw_dataset(spark: SparkSession, input_path: str) -> DataFrame:
    return (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(input_path)
    )


def clean_dataset(raw_df: DataFrame) -> DataFrame:
    return (
        raw_df
        .withColumn("vle_clicks", F.coalesce(F.col("vle_clicks"), F.lit(0)))
        .withColumn("forum_posts", F.coalesce(F.col("forum_posts"), F.lit(0)))
        .withColumn("attendance", F.coalesce(F.col("attendance"), F.lit(0)))
        .filter(F.col("student_id").isNotNull())
        .filter(F.col("module_code").isNotNull())
    )


def aggregate_by_student_module(clean_df: DataFrame) -> DataFrame:
    aggregated = (
        clean_df
        .groupBy("student_id", "module_code")
        .agg(
            F.sum("vle_clicks").alias("total_clicks"),
            F.sum("forum_posts").alias("total_posts"),
            F.avg("attendance").alias("attendance_rate"),
            F.avg(F.col("assignment_score")).alias("mean_assignment_score"),
            F.count(F.lit(1)).alias("weeks_recorded"),
        )
    )
    weight_clicks = 0.5
    weight_posts = 0.2
    weight_attendance = 0.3
    normalised = aggregated.withColumn(
        "engagement_score",
        F.round(
            (weight_clicks * (F.col("total_clicks") / F.lit(600.0)))
            + (weight_posts * (F.col("total_posts") / F.lit(40.0)))
            + (weight_attendance * F.col("attendance_rate")),
            4,
        ),
    )
    return normalised.withColumn(
        "mean_assignment_score", F.round(F.col("mean_assignment_score"), 2)
    )


def write_processed_dataset(aggregated_df: DataFrame, output_path: str) -> str:
    pandas_df = aggregated_df.orderBy("student_id", "module_code").toPandas()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pandas_df.to_csv(output_path, index=False)
    return output_path


def run_etl(
    input_path: str,
    output_path: str,
    spark: Optional[SparkSession] = None,
    stop_session: bool = True,
) -> str:
    owns_session = spark is None
    active_spark = spark or build_spark_session()
    try:
        raw_df = load_raw_dataset(active_spark, input_path)
        clean_df = clean_dataset(raw_df)
        aggregated_df = aggregate_by_student_module(clean_df)
        return write_processed_dataset(aggregated_df, output_path)
    finally:
        if owns_session and stop_session:
            active_spark.stop()
