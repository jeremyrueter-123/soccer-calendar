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
