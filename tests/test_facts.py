from knowledgeeng.facts import FactBase, build_student_facts


def test_assert_fact_returns_true_on_new_fact():
    fact_base = FactBase()
    changed = fact_base.assert_fact("engagement_level", "low")
    assert changed is True
    assert fact_base.get("engagement_level") == "low"


def test_assert_fact_returns_false_on_duplicate():
    fact_base = FactBase()
    fact_base.assert_fact("engagement_level", "low")
    changed = fact_base.assert_fact("engagement_level", "low")
    assert changed is False


def test_build_student_facts_populates_all_fields():
    fact_base = build_student_facts("S0001", "CS701", 0.8, 0.6, 55.0, 0)
    assert fact_base.get("student_id") == "S0001"
    assert fact_base.get("risk_prediction") == 0
