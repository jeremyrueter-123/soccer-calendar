from normalize import norm_time, norm_status, parse_date
from parser import grid_url


def test_time_normalization():
    assert norm_time("7:00 PM") == "19:00"
    assert norm_time("12:00 p.m.") == "12:00"
    assert norm_time("TBA") is None


def test_status_normalization():
    assert norm_status("Cancelled") == "Canceled"
    assert norm_status("No Contest") == "No Contest"


def test_grid_url():
    assert "grid=true" in grid_url("https://example.com/schedule/2026")
    assert "grid=true" in grid_url("https://example.com/schedule/2026?foo=bar")


def test_parse_date():
    assert parse_date("Oct 24", 2026).isoformat() == "2026-10-24"


def test_team_name_normalization_sidearm_variants():
    from normalize import norm_team
    assert norm_team("Mount St. Mary's (Md.)") == "Mount St. Mary's"
    assert norm_team("UMBC") == "UMBC"
    assert norm_team("University of Maryland Baltimore County") == "UMBC"
    assert norm_team("St. John's University") == "St. John's"
    assert norm_team("No. 9 Catholic University") == "Catholic"
    assert norm_team("York College of Pennsylvania") == "York (PA)"
