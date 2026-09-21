from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd


@dataclass
class TrainTestSplit:
    features_train: np.ndarray
    features_test: np.ndarray
    labels_train: np.ndarray
    labels_test: np.ndarray
    feature_names: Tuple[str, ...]


def load_processed_dataset(path: str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame = frame.dropna(subset=["mean_assignment_score"]).reset_index(drop=True)
    return frame


def make_train_test_split(
    frame: pd.DataFrame,
    feature_columns: Tuple[str, ...] = ("total_clicks", "total_posts", "attendance_rate", "engagement_score"),
    label_column: str = "at_risk",
    test_fraction: float = 0.25,
    seed: int = 7,
) -> TrainTestSplit:
    rng = np.random.default_rng(seed)
    indices = np.arange(len(frame))
    rng.shuffle(indices)
    cut = int(len(indices) * (1.0 - test_fraction))
    train_indices, test_indices = indices[:cut], indices[cut:]

    features = frame[list(feature_columns)].to_numpy(dtype=float)
    labels = frame[label_column].to_numpy(dtype=float)

    return TrainTestSplit(
        features_train=features[train_indices],
        features_test=features[test_indices],
        labels_train=labels[train_indices],
        labels_test=labels[test_indices],
        feature_names=feature_columns,
    )
