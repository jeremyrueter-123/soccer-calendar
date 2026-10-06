"""Parser for Sidearm-style official athletic schedules.

The official sites in the first wave expose a structured schedule table when
?grid=true is appended. The parser deliberately fails closed: if it cannot
confidently identify schedule rows, the source is reported as a parser issue
rather than being treated as evidence that games disappeared.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

from models import Match
from normalize import clean, norm_status, norm_team, norm_time, parse_date


@dataclass
class SourceResult:
    team: str
    gender: str
    url: str
    matches: list[Match]
    error: str | None = None


def grid_url(url: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query["grid"] = "true"
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def _headers() -> dict[str, str]:
    return {
        "User-Agent": (
            "Mozilla/5.0 (compatible; MarylandSoccerCalendarAuditor/1.0; "
            "+https://github.com/)"
        )
    }


def _header_map(table) -> dict[str, int]:
    headers = [clean(th.get_text(" ", strip=True)).lower() for th in table.select("thead th")]
    if not headers:
        first = table.find("tr")
        headers = [clean(c.get_text(" ", strip=True)).lower() for c in first.find_all(["th", "td"])] if first else []
    return {h: i for i, h in enumerate(headers)}


def _cell(cells, idx: int | None) -> str:
    if idx is None or idx >= len(cells):
        return ""
    return clean(cells[idx].get_text(" ", strip=True))


def _find_col(headers: dict[str, int], *names: str) -> int | None:
    # Exact header matches first. This is important for the short "At" column:
    # substring matching would incorrectly match "Date".
    for name in names:
        if name in headers:
            return headers[name]
    for key, idx in headers.items():
        if any(name != "at" and name in key for name in names):
            return idx
    return None


def _extract_tables(soup, source_team: str, gender: str, url: str, year: int) -> list[Match]:
    output: list[Match] = []

    for table in soup.find_all("table"):
        headers = _header_map(table)
        if not headers:
            continue

        date_i = _find_col(headers, "date")
        time_i = _find_col(headers, "time")
        at_i = _find_col(headers, "at")
        opp_i = _find_col(headers, "opponent")
        result_i = _find_col(headers, "result", "status")
        if date_i is None or opp_i is None:
            continue

        rows_found = 0
        for tr in table.select("tbody tr") or table.find_all("tr")[1:]:
            cells = tr.find_all(["td", "th"])
            if not cells:
                continue

            d = parse_date(_cell(cells, date_i), year)
            opponent = _cell(cells, opp_i)
            if not d or not opponent:
                continue

            time = norm_time(_cell(cells, time_i))
            at_value = _cell(cells, at_i).lower()
            # Sidearm's "At" column is normally Home/Away.
            away = at_value in {"away", "at"}
            opponent = norm_team(re.sub(r"^\s*#?\d+\s+", "", opponent))

            home = opponent if away else norm_team(source_team)
            away_team = norm_team(source_team) if away else opponent

            result_text = _cell(cells, result_i)
            status = norm_status(result_text)
            # If the result is a score, the game is still scheduled for audit
            # purposes; only explicit cancellation-type labels change status.
            if re.match(r"^[WLT]\b", result_text, re.I) or re.match(r"^\d", result_text):
                status = "Scheduled"

            output.append(Match(
                date=d, time=time, home=home, away=away_team,
                status=status, gender=gender, source_team=norm_team(source_team),
                source_url=url,
            ))
            rows_found += 1

        if rows_found:
            output.extend([])

    # De-duplicate identical table rows.
    unique = {}
    for m in output:
        k = (m.date, m.time, m.home, m.away, m.status, m.gender)
        unique[k] = m
    return list(unique.values())


def parse_source(source: dict, year: int = 2026) -> SourceResult:
    team, gender, url = source["team"], source["gender"], source["url"]
    target = grid_url(url)
    try:
        response = requests.get(target, headers=_headers(), timeout=30)
        response.raise_for_status()
    except Exception as exc:
        return SourceResult(team, gender, url, [], f"Fetch failed: {exc}")

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        matches = _extract_tables(soup, team, gender, url, year)
        if not matches:
            return SourceResult(team, gender, url, [], "No recognizable schedule rows found")
        return SourceResult(team, gender, url, matches)
    except Exception as exc:
        return SourceResult(team, gender, url, [], f"Parser failed: {exc}")
