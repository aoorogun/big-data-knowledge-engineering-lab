import pandas as pd
from datascience.features import add_at_risk_label, standardise_columns


def test_at_risk_label_threshold():
    frame = pd.DataFrame({"mean_assignment_score": [30.0, 60.0, 49.9, 50.0]})
    labelled = add_at_risk_label(frame)
    assert list(labelled["at_risk"]) == [1, 0, 1, 0]


def test_standardise_columns_zero_mean():
    frame = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0]})
    standardised = standardise_columns(frame, ("x",))
    assert abs(standardised["x"].mean()) < 1e-9


def test_standardise_constant_column():
    frame = pd.DataFrame({"x": [5.0, 5.0, 5.0]})
    standardised = standardise_columns(frame, ("x",))
    assert list(standardised["x"]) == [0.0, 0.0, 0.0]
