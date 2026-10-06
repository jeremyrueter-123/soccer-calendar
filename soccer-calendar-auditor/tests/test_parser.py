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


def test_sidearm_at_column_controls_home_away():
    html = """
    <table><thead><tr><th>Date</th><th>Time</th><th>Opponent</th><th>At</th><th>Result</th></tr></thead>
    <tbody>
    <tr><td>Oct 24</td><td>7:00 PM</td><td>Ursinus</td><td>Home</td><td></td></tr>
    <tr><td>Oct 25</td><td>7:00 PM</td><td>Ursinus</td><td>Away</td><td></td></tr>
    </tbody></table>
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = _extract_tables(soup, "Washington College", "Men", "https://example.com", 2026)
    assert rows[0].home == "Washington College" and rows[0].away == "Ursinus"
    assert rows[1].home == "Ursinus" and rows[1].away == "Washington College"
