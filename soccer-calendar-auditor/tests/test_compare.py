from datetime import date
from models import Match
from compare import compare_team, dedupe


def test_detects_date_change():
    cal = [Match(date(2026,10,24), "16:00", "Salisbury", "Regent", "Scheduled", "Men")]
    off = [Match(date(2026,10,21), "15:00", "Regent", "Salisbury", "Scheduled", "Men")]
    findings = compare_team(cal, off, "Salisbury", "Men")
    assert any(f["kind"] == "DATE" for f in findings)


def test_detects_time_change():
    cal = [Match(date(2026,10,24), "19:00", "Washington College", "Ursinus", "Scheduled", "Men")]
    off = [Match(date(2026,10,24), "12:00", "Ursinus", "Washington College", "Scheduled", "Men")]
    findings = compare_team(cal, off, "Washington College", "Men")
    assert any(f["kind"] == "TIME" for f in findings)


def test_detects_home_away_change():
    cal = [Match(date(2026,10,24), "12:00", "Washington College", "Ursinus", "Scheduled", "Men")]
    off = [Match(date(2026,10,24), "12:00", "Ursinus", "Washington College", "Scheduled", "Men")]
    findings = compare_team(cal, off, "Washington College", "Men")
    assert any(f["kind"] == "HOME_AWAY" for f in findings)


def test_detects_status_change():
    cal = [Match(date(2026,8,20), "13:00", "UMBC", "UNC Wilmington", "Scheduled", "Men")]
    off = [Match(date(2026,8,20), "13:00", "UMBC", "UNC Wilmington", "No Contest", "Men")]
    findings = compare_team(cal, off, "UMBC", "Men")
    assert any(f["kind"] == "STATUS" for f in findings)


def test_detects_unmatched_official_game():
    cal = []
    off = [Match(date(2026,10,24), "15:30", "Penn College", "Notre Dame (MD)", "Scheduled", "Men")]
    findings = compare_team(cal, off, "Notre Dame (MD)", "Men")
    assert any(f["kind"] == "NEW_OFFICIAL" for f in findings)


def test_deduplicates_team_side_findings():
    c = Match(date(2026,10,24), "19:00", "Washington College", "Ursinus", "Scheduled", "Men")
    o = Match(date(2026,10,24), "12:00", "Ursinus", "Washington College", "Scheduled", "Men")
    f = [
        {"kind":"TIME","team":"Washington College","calendar":c,"official":o,"detail":"Kickoff time differs"},
        {"kind":"TIME","team":"Ursinus","calendar":c,"official":o,"detail":"Kickoff time differs"},
    ]
    assert len(dedupe(f)) == 1


def test_historical_time_change_is_ignored():
    c = Match(date(2026, 9, 12), "14:00", "Hood", "Washington College", "Scheduled", "Women")
    o = Match(date(2026, 9, 12), "13:00", "Hood", "Washington College", "Scheduled", "Women")
    findings = compare_team([c], [o], "Washington College", "Women", as_of=date(2026, 10, 6))
    assert not any(f["kind"] == "TIME" for f in findings)


def test_historical_home_away_change_is_ignored():
    c = Match(date(2026, 9, 12), "14:00", "Washington College", "Hood", "Scheduled", "Women")
    o = Match(date(2026, 9, 12), "14:00", "Hood", "Washington College", "Scheduled", "Women")
    findings = compare_team([c], [o], "Washington College", "Women", as_of=date(2026, 10, 6))
    assert not any(f["kind"] == "HOME_AWAY" for f in findings)


def test_upcoming_time_change_is_still_detected():
    c = Match(date(2026, 10, 24), "19:00", "Ursinus", "Washington College", "Scheduled", "Men")
    o = Match(date(2026, 10, 24), "12:00", "Ursinus", "Washington College", "Scheduled", "Men")
    findings = compare_team([c], [o], "Washington College", "Men", as_of=date(2026, 10, 6))
    assert any(f["kind"] == "TIME" for f in findings)


def test_upcoming_home_away_change_is_still_detected():
    c = Match(date(2026, 10, 24), "12:00", "Washington College", "Ursinus", "Scheduled", "Men")
    o = Match(date(2026, 10, 24), "12:00", "Ursinus", "Washington College", "Scheduled", "Men")
    findings = compare_team([c], [o], "Washington College", "Men", as_of=date(2026, 10, 6))
    assert any(f["kind"] == "HOME_AWAY" for f in findings)


def test_historical_missing_calendar_game_is_review():
    from compare import severity
    c = Match(date(2026, 9, 1), "18:00", "Team A", "Team B", "Scheduled", "Men")
    assert severity("MISSING_OFFICIAL", c, None) == "YELLOW"


def test_upcoming_missing_calendar_game_is_actionable():
    from compare import severity
    c = Match(date(2026, 10, 24), "18:00", "Team A", "Team B", "Scheduled", "Men")
    assert severity("MISSING_OFFICIAL", c, None) == "RED"


def test_duplicate_calendar_entries_are_detected():
    from compare import find_calendar_duplicates
    a = Match(date(2026, 10, 3), "16:00", "Notre Dame (MD)", "Valley Forge", "Scheduled", "Men")
    b = Match(date(2026, 10, 3), None, "Notre Dame (MD)", "Valley Forge", "Scheduled", "Men")
    findings = find_calendar_duplicates([a, b])
    assert len(findings) == 1
    assert findings[0]["kind"] == "DUPLICATE_CALENDAR"
