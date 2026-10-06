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
