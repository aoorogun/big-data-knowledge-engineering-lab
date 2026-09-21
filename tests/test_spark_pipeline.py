import os
import tempfile

import pytest

from dataeng.spark_pipeline import build_spark_session, run_etl
from dataeng.synthetic_data import generate_dataset


@pytest.fixture(scope="module")
def spark_session():
    session = build_spark_session(app_name="test_session")
    yield session
    session.stop()


def test_run_etl_produces_expected_columns(spark_session, tmp_path):
    raw_path = os.path.join(tmp_path, "raw.csv")
    processed_path = os.path.join(tmp_path, "processed.csv")
    generate_dataset(raw_path, number_of_students=6, seed=3)

    run_etl(raw_path, processed_path, spark=spark_session, stop_session=False)

    with open(processed_path, "r", encoding="utf-8") as handle:
        header = handle.readline().strip().split(",")

    expected_columns = {
        "student_id", "module_code", "total_clicks", "total_posts",
        "attendance_rate", "mean_assignment_score", "weeks_recorded", "engagement_score",
    }
    assert expected_columns.issubset(set(header))


def test_run_etl_row_count_matches_students_and_modules(spark_session, tmp_path):
    raw_path = os.path.join(tmp_path, "raw.csv")
    processed_path = os.path.join(tmp_path, "processed.csv")
    generate_dataset(raw_path, number_of_students=4, seed=8)

    run_etl(raw_path, processed_path, spark=spark_session, stop_session=False)

    with open(processed_path, "r", encoding="utf-8") as handle:
        row_count = sum(1 for _ in handle) - 1

    assert row_count == 4 * 3
