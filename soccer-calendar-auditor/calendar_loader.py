"""Load the published Google Sheet/CSV into normalized matches."""
from __future__ import annotations

import csv
from pathlib import Path
from urllib.request import Request, urlopen

from models import Match
from normalize import norm_status, norm_team, norm_time, parse_date


def _read_text(source: str) -> str:
    if source.startswith(("http://", "https://")):
        req = Request(source, headers={"User-Agent": "Mozilla/5.0 schedule-auditor"})
        with urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8-sig")
    return Path(source).read_text(encoding="utf-8-sig")


def load_calendar(source: str) -> list[Match]:
    text = _read_text(source)
    rows = csv.DictReader(text.splitlines())
    matches = []
    for row in rows:
        include = (row.get("Include") or row.get("include") or "Yes").strip().lower()
        if include != "yes":
            continue

        d = parse_date(row.get("Date", ""), 2026)
        if not d:
            continue

        home = norm_team(row.get("Home Team") or row.get("home"))
        away = norm_team(row.get("Away Team") or row.get("away"))
        if not home or not away:
            continue

        matches.append(Match(
            date=d,
            time=norm_time(row.get("Time") or row.get("time")),
            home=home,
            away=away,
            status=norm_status(row.get("Match Status") or row.get("status")),
            gender=(row.get("Gender") or row.get("gender") or "").strip() or None,
        ))
    return matches
