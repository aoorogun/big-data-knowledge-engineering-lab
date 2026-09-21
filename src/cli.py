from __future__ import annotations
import argparse
import json
import os

from dataeng.spark_pipeline import run_etl
from dataeng.synthetic_data import generate_dataset
from pipeline import run_full_pipeline

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RAW_PATH = os.path.join(REPO_ROOT, "data", "raw", "engagement.csv")
DEFAULT_PROCESSED_PATH = os.path.join(REPO_ROOT, "data", "processed", "aggregated.csv")


def _generate_data_command(args: argparse.Namespace) -> None:
    path = generate_dataset(args.output, number_of_students=args.students, seed=args.seed)
    print(f"Synthetic dataset written to {path}")


def _run_etl_command(args: argparse.Namespace) -> None:
    path = run_etl(args.input, args.output)
    print(f"Processed dataset written to {path}")


def _run_all_command(args: argparse.Namespace) -> None:
    result = run_full_pipeline(number_of_students=args.students, seed=args.seed)
    summary = {
        "raw_data_path": result.raw_data_path,
        "processed_data_path": result.processed_data_path,
        "report_path": result.report_path,
        "metrics": {
            "accuracy": result.metrics.accuracy,
            "precision": result.metrics.precision,
            "recall": result.metrics.recall,
            "f1_score": result.metrics.f1_score,
        },
        "r_statistics_available": bool(result.r_statistics),
    }
    print(json.dumps(summary, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate-data")
    generate_parser.add_argument("--output", default=DEFAULT_RAW_PATH)
    generate_parser.add_argument("--students", type=int, default=120)
    generate_parser.add_argument("--seed", type=int, default=42)
    generate_parser.set_defaults(func=_generate_data_command)

    etl_parser = subparsers.add_parser("run-etl")
    etl_parser.add_argument("--input", default=DEFAULT_RAW_PATH)
    etl_parser.add_argument("--output", default=DEFAULT_PROCESSED_PATH)
    etl_parser.set_defaults(func=_run_etl_command)

    run_all_parser = subparsers.add_parser("run-all")
    run_all_parser.add_argument("--students", type=int, default=120)
    run_all_parser.add_argument("--seed", type=int, default=42)
    run_all_parser.set_defaults(func=_run_all_command)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
