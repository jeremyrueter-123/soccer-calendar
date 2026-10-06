from datetime import date

from models import Match
from normalize import norm_status, norm_team
from compare import find_calendar_duplicates


def test_institutional_suffixes():
    assert norm_team("Alvernia") == norm_team("Alvernia University")
    assert norm_team("Hartwick") == norm_team("Hartwick College")
    assert norm_team("Bryn Mawr") == norm_team("Bryn Mawr College")
    assert norm_team("Gettysburg") == norm_team("Gettysburg College")


def test_state_suffixes():
    assert norm_team("Bridgewater") == norm_team("Bridgewater (Va.)")
    assert norm_team("Mount St. Mary's") == norm_team("Mount St. Mary's (Md.)")


def test_distinct_washington_names():
    assert norm_team("Washington College") == norm_team("Washington (Md.)")


def test_common_abbreviations():
    assert norm_team("FDU") == norm_team("Fairleigh Dickinson")
    assert norm_team("Army") == norm_team("Army West Point")


def test_dash_status():
    assert norm_status("-") == "Scheduled"
    assert norm_status("—") == "Scheduled"


def test_duplicate_calendar_entries():
    a = Match(date(2026,10,3), "16:00", "Notre Dame (MD)", "Valley Forge", "Scheduled", "Men")
    b = Match(date(2026,10,3), None, "Notre Dame (MD)", "Valley Forge", "Scheduled", "Men")
    findings = find_calendar_duplicates([a, b])
    assert len(findings) == 1


def test_display_team_cleans_report_names():
    from normalize import display_team
    assert display_team("st mary s") == "St. Mary's"
    assert display_team("notre dame") == "Notre Dame (MD)"
    assert display_team("james madison") == "James Madison"


def test_duplicate_groups_do_not_cross_gender():
    from datetime import date
    from models import Match
    from compare import find_calendar_duplicates
    men = Match(date(2026, 10, 3), "16:00", "Notre Dame (MD)", "Valley Forge", "Scheduled", "Men")
    women = Match(date(2026, 10, 3), None, "Notre Dame (MD)", "Valley Forge", "Scheduled", "Women")
    assert find_calendar_duplicates([men, women]) == []


def test_display_team_uses_canonical_aliases():
    from normalize import display_team
    assert display_team("Notre Dame (md)") == "Notre Dame (MD)"
    assert display_team("Mcdaniel") == "McDaniel"
    assert display_team("UMBC") == "UMBC"
    assert display_team("York (pa)") == "York (PA)"
    assert display_team("St Mary S College Of Maryland") == "St. Mary's"


def test_washington_college_alias():
    assert norm_team("Washington") == "Washington College"
    assert norm_team("Washington College") == "Washington College"
