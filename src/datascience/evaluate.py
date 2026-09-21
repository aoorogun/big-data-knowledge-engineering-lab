from __future__ import annotations
from dataclasses import dataclass

import numpy as np


@dataclass
class ClassificationMetrics:
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    true_positive: int
    true_negative: int
    false_positive: int
    false_negative: int


def evaluate_predictions(labels_true: np.ndarray, labels_predicted: np.ndarray) -> ClassificationMetrics:
    true_positive = int(np.sum((labels_predicted == 1) & (labels_true == 1)))
    true_negative = int(np.sum((labels_predicted == 0) & (labels_true == 0)))
    false_positive = int(np.sum((labels_predicted == 1) & (labels_true == 0)))
    false_negative = int(np.sum((labels_predicted == 0) & (labels_true == 1)))

    total = true_positive + true_negative + false_positive + false_negative
    accuracy = (true_positive + true_negative) / total if total else 0.0
    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) else 0.0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) else 0.0
    f1_score = (
        2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    )

    return ClassificationMetrics(
        accuracy=round(accuracy, 4),
        precision=round(precision, 4),
        recall=round(recall, 4),
        f1_score=round(f1_score, 4),
        true_positive=true_positive,
        true_negative=true_negative,
        false_positive=false_positive,
        false_negative=false_negative,
    )
