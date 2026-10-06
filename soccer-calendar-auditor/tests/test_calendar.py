from calendar_loader import load_calendar


def test_load_calendar():
    rows = load_calendar("tests/fixtures/sample_calendar.csv")
    assert len(rows) == 3
    assert rows[0].home == "Washington College"
    assert rows[0].time == "19:00"
