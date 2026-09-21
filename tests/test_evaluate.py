import numpy as np
from datascience.evaluate import evaluate_predictions


def test_perfect_predictions():
    labels_true = np.array([1, 0, 1, 0])
    labels_predicted = np.array([1, 0, 1, 0])
    metrics = evaluate_predictions(labels_true, labels_predicted)
    assert metrics.accuracy == 1.0
    assert metrics.precision == 1.0
    assert metrics.recall == 1.0
    assert metrics.f1_score == 1.0


def test_all_wrong_predictions():
    labels_true = np.array([1, 1, 0, 0])
    labels_predicted = np.array([0, 0, 1, 1])
    metrics = evaluate_predictions(labels_true, labels_predicted)
    assert metrics.accuracy == 0.0
    assert metrics.true_positive == 0
