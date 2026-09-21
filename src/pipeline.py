from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Dict, List

from dataeng.spark_pipeline import run_etl
from dataeng.synthetic_data import generate_dataset
from datascience.dataset import load_processed_dataset, make_train_test_split
from datascience.evaluate import ClassificationMetrics, evaluate_predictions
from datascience.features import add_at_risk_label
from datascience.model import train_logistic_regression
from knowledgeeng.facts import build_student_facts
from knowledgeeng.inference_engine import collect_recommendations, run_forward_chaining
from knowledgeeng.rules import build_default_rule_set
from r_integration import run_statistical_analysis
from reporting.report_builder import StudentRecommendation, build_report, write_report

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@dataclass
class PipelineResult:
    raw_data_path: str
    processed_data_path: str
    report_path: str
    metrics: ClassificationMetrics
    recommendations: List[StudentRecommendation]
    r_statistics: Dict[str, str]


def run_full_pipeline(
    raw_data_path: str = None,
    processed_data_path: str = None,
    report_path: str = None,
    number_of_students: int = 120,
    seed: int = 42,
) -> PipelineResult:
    raw_data_path = raw_data_path or os.path.join(REPO_ROOT, "data", "raw", "engagement.csv")
    processed_data_path = processed_data_path or os.path.join(REPO_ROOT, "data", "processed", "aggregated.csv")
    report_path = report_path or os.path.join(REPO_ROOT, "outputs", "report.md")
    r_script_path = os.path.join(REPO_ROOT, "r", "statistical_analysis.R")
    r_output_path = os.path.join(REPO_ROOT, "outputs", "r_statistics.txt")

    generate_dataset(raw_data_path, number_of_students=number_of_students, seed=seed)
    with open(raw_data_path, "r", encoding="utf-8") as raw_file:
        raw_record_count = sum(1 for _ in raw_file) - 1
    run_etl(raw_data_path, processed_data_path)

    frame = load_processed_dataset(processed_data_path)
    frame = add_at_risk_label(frame)
    split = make_train_test_split(frame)

    model = train_logistic_regression(split.features_train, split.labels_train)
    predictions = model.predict(split.features_test)
    metrics = evaluate_predictions(split.labels_test, predictions)

    all_predictions = model.predict(frame[list(split.feature_names)].to_numpy(dtype=float))
    frame = frame.assign(risk_prediction=all_predictions)

    rule_set = build_default_rule_set()
    recommendations: List[StudentRecommendation] = []
    for _, row in frame.iterrows():
        facts = build_student_facts(
            student_id=row["student_id"],
            module_code=row["module_code"],
            attendance_rate=row["attendance_rate"],
            engagement_score=row["engagement_score"],
            mean_assignment_score=row["mean_assignment_score"],
            risk_prediction=int(row["risk_prediction"]),
        )
        run_forward_chaining(facts, rule_set)
        recommendations.append(
            StudentRecommendation(
                student_id=facts.get("student_id"),
                module_code=facts.get("module_code"),
                engagement_level=facts.get("engagement_level", "unknown"),
                recommendations=collect_recommendations(facts),
            )
        )

    r_statistics = run_statistical_analysis(processed_data_path, r_output_path, r_script_path)

    report_text = build_report(
        number_of_records=raw_record_count,
        number_of_students=len(frame),
        metrics=metrics,
        student_recommendations=recommendations,
        r_statistics=r_statistics,
    )
    write_report(report_text, report_path)

    return PipelineResult(
        raw_data_path=raw_data_path,
        processed_data_path=processed_data_path,
        report_path=report_path,
        metrics=metrics,
        recommendations=recommendations,
        r_statistics=r_statistics,
    )
