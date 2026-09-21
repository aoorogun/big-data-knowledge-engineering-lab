from __future__ import annotations
import os
import shutil
import subprocess
from typing import Dict


def r_available() -> bool:
    return shutil.which("Rscript") is not None


def run_statistical_analysis(processed_csv_path: str, output_txt_path: str, script_path: str) -> Dict[str, str]:
    if not r_available():
        return {}
    os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
    subprocess.run(
        ["Rscript", script_path, processed_csv_path, output_txt_path],
        check=True,
        capture_output=True,
        text=True,
    )
    results: Dict[str, str] = {}
    with open(output_txt_path, "r", encoding="utf-8") as handle:
        for line in handle:
            if ":" in line:
                key, _, value = line.partition(":")
                results[key.strip()] = value.strip()
    return results
