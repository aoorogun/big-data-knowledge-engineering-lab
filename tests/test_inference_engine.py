from knowledgeeng.facts import build_student_facts
from knowledgeeng.inference_engine import collect_recommendations, run_forward_chaining
from knowledgeeng.rules import build_default_rule_set


def test_forward_chaining_produces_tutor_referral():
    facts = build_student_facts(
        student_id="S0099",
        module_code="CS701",
        attendance_rate=0.9,
        engagement_score=0.1,
        mean_assignment_score=35.0,
        risk_prediction=1,
    )
    rules = build_default_rule_set()
    run_forward_chaining(facts, rules)
    recommendations = collect_recommendations(facts)
    assert any("tutor" in message.lower() for message in recommendations)


def test_forward_chaining_produces_no_action_for_healthy_student():
    facts = build_student_facts(
        student_id="S0100",
        module_code="CS702",
        attendance_rate=0.95,
        engagement_score=0.9,
        mean_assignment_score=85.0,
        risk_prediction=0,
    )
    rules = build_default_rule_set()
    run_forward_chaining(facts, rules)
    recommendations = collect_recommendations(facts)
    assert any("no intervention" in message.lower() for message in recommendations)
