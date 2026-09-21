from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Dict, List

from datascience.evaluate import ClassificationMetrics


@dataclass
class StudentRecommendation:
    student_id: str
    module_code: str
    engagement_level: str
    recommendations: List[str]


def build_report(
    number_of_records: int,
    number_of_students: int,
    metrics: ClassificationMetrics,
    student_recommendations: List[StudentRecommendation],
    r_statistics: Dict[str, str],
) -> str:
    lines: List[str] = []
    lines.append("# Student Engagement Analytics Report")
    lines.append("")
    lines.append("## Pipeline Summary")
    lines.append(f"- Raw weekly records processed: {number_of_records}")
    lines.append(f"- Distinct student-module records aggregated: {number_of_students}")
    lines.append("")
    lines.append("## At-Risk Classification Model")
    lines.append(f"- Accuracy: {metrics.accuracy}")
    lines.append(f"- Precision: {metrics.precision}")
    lines.append(f"- Recall: {metrics.recall}")
    lines.append(f"- F1 score: {metrics.f1_score}")
    lines.append(
        f"- Confusion matrix: TP={metrics.true_positive}, TN={metrics.true_negative}, "
        f"FP={metrics.false_positive}, FN={metrics.false_negative}"
    )
    lines.append("")
    if r_statistics:
        lines.append("## R Statistical Analysis")
        for key, value in r_statistics.items():
            lines.append(f"- {key}: {value}")
        lines.append("")
    lines.append("## Knowledge Engineering Recommendations (sample)")
    for recommendation in student_recommendations[:10]:
        joined = "; ".join(recommendation.recommendations)
        lines.append(
            f"- {recommendation.student_id} ({recommendation.module_code}, "
            f"{recommendation.engagement_level} engagement): {joined}"
        )
    return "\n".join(lines)


def write_report(report_text: str, output_path: str) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(report_text)
    return output_path
