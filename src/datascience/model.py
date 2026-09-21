from __future__ import annotations
from dataclasses import dataclass

import numpy as np


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


@dataclass
class LogisticRegressionModel:
    weights: np.ndarray
    bias: float

    def predict_probabilities(self, features: np.ndarray) -> np.ndarray:
        return _sigmoid(features @ self.weights + self.bias)

    def predict(self, features: np.ndarray, threshold: float = 0.5) -> np.ndarray:
        return (self.predict_probabilities(features) >= threshold).astype(int)


def train_logistic_regression(
    features: np.ndarray,
    labels: np.ndarray,
    learning_rate: float = 0.05,
    epochs: int = 2000,
    l2_penalty: float = 0.001,
) -> LogisticRegressionModel:
    number_of_samples, number_of_features = features.shape
    feature_means = features.mean(axis=0)
    feature_stds = features.std(axis=0)
    feature_stds[feature_stds == 0] = 1.0
    normalised_features = (features - feature_means) / feature_stds

    weights = np.zeros(number_of_features)
    bias = 0.0

    for _ in range(epochs):
        linear_output = normalised_features @ weights + bias
        predictions = _sigmoid(linear_output)
        error = predictions - labels

        weight_gradient = (normalised_features.T @ error) / number_of_samples + l2_penalty * weights
        bias_gradient = float(np.mean(error))

        weights -= learning_rate * weight_gradient
        bias -= learning_rate * bias_gradient

    rescaled_weights = weights / feature_stds
    rescaled_bias = bias - float(np.sum(weights * feature_means / feature_stds))

    return LogisticRegressionModel(weights=rescaled_weights, bias=rescaled_bias)
