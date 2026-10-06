from datetime import date
from models import Match
from compare import duplicate_findings, compare

def m(d, t, home, away, status="Scheduled", team="Notre Dame (MD)"):
    return Match(date.fromisoformat(d), t, home, away, status, "Men", team, "x")

def test_duplicate_calendar_entries():
    rows = [
        m("2026-10-03", "16:00", "Notre Dame (MD)", "Valley Forge"),
        m("2026-10-03", None, "Notre Dame (MD)", "Valley Forge"),
    ]
    findings = duplicate_findings(rows)
    assert len(findings) == 1
    assert "Duplicate calendar entries" in findings[0].issue

def test_dash_status_does_not_flag():
    cm = m("2026-10-10", "16:00", "Maryland", "Nebraska", "Scheduled", "Maryland")
    om = m("2026-10-10", "16:00", "Maryland", "Nebraska", "-", "Maryland")
    findings = compare([cm], [om], "Maryland", date(2026,10,1))
    assert not any("status" in f.issue.lower() for f in findings)

def test_historical_missing_is_review():
    cm = m("2026-09-01", "16:00", "Team A", "Maryland", "Scheduled", "Maryland")
    findings = compare([cm], [], "Maryland", date(2026,10,1))
    assert findings[0].severity == "YELLOW"
