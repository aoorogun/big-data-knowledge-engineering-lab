from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Set


@dataclass
class FactBase:
    facts: Dict[str, Any] = field(default_factory=dict)

    def assert_fact(self, key: str, value: Any) -> bool:
        if key in self.facts and self.facts[key] == value:
            return False
        self.facts[key] = value
        return True

    def has(self, key: str) -> bool:
        return key in self.facts

    def get(self, key: str, default: Any = None) -> Any:
        return self.facts.get(key, default)

    def keys(self) -> Set[str]:
        return set(self.facts.keys())


def build_student_facts(
    student_id: str,
    module_code: str,
    attendance_rate: float,
    engagement_score: float,
    mean_assignment_score: float,
    risk_prediction: int,
) -> FactBase:
    fact_base = FactBase()
    fact_base.assert_fact("student_id", student_id)
    fact_base.assert_fact("module_code", module_code)
    fact_base.assert_fact("attendance_rate", attendance_rate)
    fact_base.assert_fact("engagement_score", engagement_score)
    fact_base.assert_fact("mean_assignment_score", mean_assignment_score)
    fact_base.assert_fact("risk_prediction", risk_prediction)
    return fact_base
