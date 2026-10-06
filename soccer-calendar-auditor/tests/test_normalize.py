from normalize import norm_team, norm_status

def test_institutional_suffixes():
    assert norm_team("Alvernia") == norm_team("Alvernia University")
    assert norm_team("Hartwick") == norm_team("Hartwick College")
    assert norm_team("Bryn Mawr") == norm_team("Bryn Mawr College")
    assert norm_team("Gettysburg") == norm_team("Gettysburg College")

def test_state_suffixes():
    assert norm_team("Bridgewater") == norm_team("Bridgewater (Va.)")
    assert norm_team("Washington College") != norm_team("Washington (Md.)")

def test_abbreviations():
    assert norm_team("FDU") == norm_team("Fairleigh Dickinson")
    assert norm_team("Army") == norm_team("Army West Point")

def test_maryland_dash_status():
    assert norm_status("-") == "Scheduled"
    assert norm_status("—") == "Scheduled"
