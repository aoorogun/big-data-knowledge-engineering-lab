import numpy as np
from datascience.model import train_logistic_regression


def test_model_separates_linearly_separable_data():
    features = np.array([[0.0], [0.1], [0.2], [5.0], [5.1], [5.2]])
    labels = np.array([0, 0, 0, 1, 1, 1])
    model = train_logistic_regression(features, labels, epochs=3000)
    predictions = model.predict(features)
    assert list(predictions) == list(labels)


def test_predict_probabilities_in_unit_interval():
    features = np.array([[0.0], [1.0], [2.0]])
    labels = np.array([0, 0, 1])
    model = train_logistic_regression(features, labels, epochs=500)
    probabilities = model.predict_probabilities(features)
    assert all(0.0 <= p <= 1.0 for p in probabilities)
