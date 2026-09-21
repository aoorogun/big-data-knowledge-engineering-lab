from __future__ import annotations
import pandas as pd

AT_RISK_SCORE_THRESHOLD = 50.0


def add_at_risk_label(frame: pd.DataFrame, threshold: float = AT_RISK_SCORE_THRESHOLD) -> pd.DataFrame:
    enriched = frame.copy()
    enriched["at_risk"] = (enriched["mean_assignment_score"] < threshold).astype(int)
    return enriched


def standardise_columns(frame: pd.DataFrame, columns: tuple) -> pd.DataFrame:
    standardised = frame.copy()
    for column in columns:
        mean = standardised[column].mean()
        std = standardised[column].std()
        if std == 0:
            standardised[column] = 0.0
        else:
            standardised[column] = (standardised[column] - mean) / std
    return standardised
