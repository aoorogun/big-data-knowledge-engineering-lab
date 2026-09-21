from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from knowledgeeng.facts import FactBase
from knowledgeeng.rules import Rule


@dataclass
class InferenceTrace:
    fired_rules: List[str] = field(default_factory=list)


def run_forward_chaining(
    facts: FactBase,
    rules: List[Rule],
    max_iterations: int = 50,
) -> InferenceTrace:
    trace = InferenceTrace()
    for _ in range(max_iterations):
        fired_this_round = False
        for rule in rules:
            if rule.condition(facts):
                rule.action(facts)
                trace.fired_rules.append(rule.name)
                fired_this_round = True
        if not fired_this_round:
            break
    return trace


def collect_recommendations(facts: FactBase) -> List[str]:
    recommendation_flags = {
        "recommend_tutor_referral": "Refer to personal tutor for a wellbeing and study skills check-in.",
        "recommend_attendance_meeting": "Schedule an attendance monitoring meeting.",
        "recommend_formative_feedback": "Offer a formative feedback session ahead of the next assessment.",
        "recommend_no_action": "No intervention required at this time.",
    }
    return [
        message
        for flag, message in recommendation_flags.items()
        if facts.get(flag)
    ]
