from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, List

from knowledgeeng.facts import FactBase


@dataclass
class Rule:
    name: str
    condition: Callable[[FactBase], bool]
    action: Callable[[FactBase], None]


def _engagement_level_rule() -> Rule:
    def condition(facts: FactBase) -> bool:
        return facts.has("engagement_score") and not facts.has("engagement_level")

    def action(facts: FactBase) -> None:
        score = facts.get("engagement_score")
        if score < 0.35:
            level = "low"
        elif score < 0.65:
            level = "medium"
        else:
            level = "high"
        facts.assert_fact("engagement_level", level)

    return Rule(name="derive_engagement_level", condition=condition, action=action)


def _low_attendance_rule() -> Rule:
    def condition(facts: FactBase) -> bool:
        return facts.get("attendance_rate", 1.0) < 0.5 and not facts.has("recommend_attendance_meeting")

    def action(facts: FactBase) -> None:
        facts.assert_fact("recommend_attendance_meeting", True)

    return Rule(name="flag_low_attendance", condition=condition, action=action)


def _borderline_score_rule() -> Rule:
    def condition(facts: FactBase) -> bool:
        score = facts.get("mean_assignment_score")
        return (
            score is not None
            and 40.0 <= score < 50.0
            and not facts.has("recommend_formative_feedback")
        )

    def action(facts: FactBase) -> None:
        facts.assert_fact("recommend_formative_feedback", True)

    return Rule(name="flag_borderline_score", condition=condition, action=action)


def _tutor_referral_rule() -> Rule:
    def condition(facts: FactBase) -> bool:
        return (
            facts.get("engagement_level") == "low"
            and facts.get("risk_prediction") == 1
            and not facts.has("recommend_tutor_referral")
        )

    def action(facts: FactBase) -> None:
        facts.assert_fact("recommend_tutor_referral", True)

    return Rule(name="flag_tutor_referral", condition=condition, action=action)


def _no_action_needed_rule() -> Rule:
    def condition(facts: FactBase) -> bool:
        already_flagged = any(
            facts.get(key) for key in (
                "recommend_attendance_meeting",
                "recommend_formative_feedback",
                "recommend_tutor_referral",
            )
        )
        return (
            facts.has("engagement_level")
            and facts.get("risk_prediction") == 0
            and not already_flagged
            and not facts.has("recommend_no_action")
        )

    def action(facts: FactBase) -> None:
        facts.assert_fact("recommend_no_action", True)

    return Rule(name="flag_no_action_needed", condition=condition, action=action)


def build_default_rule_set() -> List[Rule]:
    return [
        _engagement_level_rule(),
        _low_attendance_rule(),
        _borderline_score_rule(),
        _tutor_referral_rule(),
        _no_action_needed_rule(),
    ]
