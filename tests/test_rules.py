from knowledgeeng.facts import FactBase
from knowledgeeng.rules import build_default_rule_set


def test_engagement_level_rule_fires_once():
    facts = FactBase()
    facts.assert_fact("engagement_score", 0.2)
    facts.assert_fact("attendance_rate", 0.9)
    facts.assert_fact("mean_assignment_score", 70.0)
    facts.assert_fact("risk_prediction", 0)

    rules = build_default_rule_set()
    engagement_rule = next(r for r in rules if r.name == "derive_engagement_level")
    assert engagement_rule.condition(facts) is True
    engagement_rule.action(facts)
    assert facts.get("engagement_level") == "low"
    assert engagement_rule.condition(facts) is False


def test_low_attendance_rule():
    facts = FactBase()
    facts.assert_fact("attendance_rate", 0.3)
    rules = build_default_rule_set()
    attendance_rule = next(r for r in rules if r.name == "flag_low_attendance")
    assert attendance_rule.condition(facts) is True
