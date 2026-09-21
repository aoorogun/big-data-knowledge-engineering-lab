from dataeng.synthetic_data import generate_records


def test_record_count_matches_students_modules_weeks():
    records = generate_records(number_of_students=5, seed=1)
    assert len(records) == 5 * 3 * 12


def test_assignment_score_only_on_assessment_weeks():
    records = generate_records(number_of_students=2, seed=1)
    for record in records:
        if record["week_number"] in (4, 8, 12):
            assert record["assignment_score"] != ""
        else:
            assert record["assignment_score"] == ""


def test_deterministic_with_same_seed():
    first = generate_records(number_of_students=3, seed=99)
    second = generate_records(number_of_students=3, seed=99)
    assert first == second
