import os

from pipeline import run_full_pipeline


def test_full_pipeline_runs_end_to_end(tmp_path):
    raw_path = os.path.join(tmp_path, "raw.csv")
    processed_path = os.path.join(tmp_path, "processed.csv")
    report_path = os.path.join(tmp_path, "report.md")

    result = run_full_pipeline(
        raw_data_path=raw_path,
        processed_data_path=processed_path,
        report_path=report_path,
        number_of_students=30,
        seed=5,
    )

    assert os.path.exists(result.report_path)
    assert result.metrics.accuracy >= 0.0
    assert len(result.recommendations) == 30 * 3
