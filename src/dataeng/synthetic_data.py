from __future__ import annotations
import csv
import os
from typing import List

import numpy as np

MODULE_CODES = ["CS701", "CS702", "CS703"]
ASSESSMENT_WEEKS = {4, 8, 12}
TOTAL_WEEKS = 12
FIELDNAMES = [
    "student_id",
    "module_code",
    "week_number",
    "vle_clicks",
    "forum_posts",
    "attendance",
    "assignment_score",
]


def generate_records(number_of_students: int = 120, seed: int = 42) -> List[dict]:
    rng = np.random.default_rng(seed)
    records: List[dict] = []
    for student_index in range(number_of_students):
        student_id = f"S{student_index + 1:04d}"
        baseline_engagement = rng.beta(2.0, 2.0)
        for module_code in MODULE_CODES:
            module_shift = rng.normal(0.0, 0.05)
            for week_number in range(1, TOTAL_WEEKS + 1):
                weekly_noise = rng.normal(0.0, 0.1)
                engagement_level = float(np.clip(baseline_engagement + module_shift + weekly_noise, 0.0, 1.0))
                vle_clicks = int(rng.poisson(lam=5 + engagement_level * 40))
                forum_posts = int(rng.poisson(lam=engagement_level * 3))
                attendance = 1 if rng.random() < (0.5 + engagement_level * 0.45) else 0
                assignment_score = ""
                if week_number in ASSESSMENT_WEEKS:
                    raw_score = 30 + engagement_level * 65 + rng.normal(0.0, 6.0)
                    assignment_score = round(float(np.clip(raw_score, 0.0, 100.0)), 1)
                records.append({
                    "student_id": student_id,
                    "module_code": module_code,
                    "week_number": week_number,
                    "vle_clicks": vle_clicks,
                    "forum_posts": forum_posts,
                    "attendance": attendance,
                    "assignment_score": assignment_score,
                })
    return records


def write_records(records: List[dict], output_path: str) -> str:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)
    return output_path


def generate_dataset(output_path: str, number_of_students: int = 120, seed: int = 42) -> str:
    records = generate_records(number_of_students=number_of_students, seed=seed)
    return write_records(records, output_path)
