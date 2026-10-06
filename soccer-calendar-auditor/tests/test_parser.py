from pathlib import Path
from bs4 import BeautifulSoup
from parser import _extract_tables


def test_sidearm_table_parser():
    html = Path("tests/fixtures/sample_schedule.html").read_text()
    soup = BeautifulSoup(html, "html.parser")
    rows = _extract_tables(
        soup, "Washington College", "Men",
        "https://example.com/schedule/2026", 2026
    )
    assert len(rows) == 2
    assert rows[0].home == "Washington College"
    assert rows[0].away == "Ursinus"
    assert rows[1].home == "Gettysburg"
    assert rows[1].away == "Washington College"
