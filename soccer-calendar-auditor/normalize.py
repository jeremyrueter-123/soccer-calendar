"""Normalization helpers shared by calendar and official parsers."""
from __future__ import annotations

import re
from datetime import date, datetime

from config import STATUS_ALIASES, TEAM_ALIASES


def clean(value: str | None) -> str:
    s = (value or "").replace("\xa0", " ")
    # Sidearm frequently uses asterisks as footnote/ranking markers.
    s = s.replace("*", " ")
    return re.sub(r"\s+", " ", s).strip()


def _team_key(value: str | None) -> str:
    s = clean(value).lower()
    # Remove ranking prefixes such as "No. 9" or "RV".
    s = re.sub(r"^(?:no\.?\s*\d+|#\s*\d+|rv)\s+", "", s)
    # Remove state/location parentheticals commonly appended by athletic sites.
    s = re.sub(
        r"\s*\((?:md|pa|va|dc|nj|ny|de|ma|ct|ri|nc|sc|wv|oh|ohio|mi|il|in|wi|mn|ky|tn|al|ga|tx|ca|calif|colo|ore|wash|az|ariz)\.?\)\s*$",
        "",
        s,
    )
    # Normalize common abbreviations before punctuation cleanup.
    s = re.sub(r"\buniv\.?\b", "university", s)
    s = re.sub(r"\bu\.?\b", "university", s)
    s = re.sub(r"\bcol\.?\b", "college", s)
    # Remove common academic suffixes that do not distinguish the team.
    s = re.sub(r"\s+(?:university|college|school)$", "", s)
    # Normalize punctuation before alias lookup.
    s = re.sub(r"[^a-z0-9 ]+", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def norm_team(value: str | None) -> str:
    raw = clean(value)
    key = _team_key(raw)
    if not key:
        return ""

    # Exact configured aliases first.
    if key in TEAM_ALIASES:
        return TEAM_ALIASES[key]

    # Common "University of ..." pattern.
    if key.startswith("university of "):
        shortened = key[len("university of "):]
        if shortened in TEAM_ALIASES:
            return TEAM_ALIASES[shortened]

    return raw


def norm_time(value: str | None) -> str | None:
    s = clean(value).lower().replace(".", "")
    if not s or s in {"tba", "tbd", "-", "—", "n/a"}:
        return None
    if s == "noon":
        return "12:00"
    if s == "midnight":
        return "00:00"
    s = re.sub(r"\s+et$", "", s)
    m = re.match(r"^(\d{1,2})(?::(\d{2})(?::\d{2})?)?\s*(am|pm)?$", s)
    if not m:
        return s
    h = int(m.group(1))
    minute = int(m.group(2) or 0)
    ap = m.group(3)
    if ap == "pm" and h != 12:
        h += 12
    if ap == "am" and h == 12:
        h = 0
    return f"{h:02d}:{minute:02d}"


def norm_status(value: str | None) -> str:
    s = clean(value)
    if not s:
        return "Scheduled"
    low = s.lower()
    return STATUS_ALIASES.get(low, s)


def parse_date(value: str, year: int) -> date | None:
    s = clean(value)
    if not s:
        return None

    formats = [
        "%Y-%m-%d",
        "%B %d, %Y", "%b %d, %Y",
        "%m/%d/%Y", "%m/%d/%y",
    ]
    for fmt in formats:
        try:
            d = datetime.strptime(s, fmt).date()
            if "%Y" not in fmt and "%y" not in fmt:
                d = d.replace(year=year)
            return d
        except ValueError:
            pass

    m = re.match(r"^([A-Za-z]+)\s+(\d{1,2})", s)
    if m:
        for fmt in ("%b %d", "%B %d"):
            try:
                d = datetime.strptime(f"{year} {m.group(1)} {m.group(2)}", f"%Y {fmt}").date()
                return d
            except ValueError:
                pass
    return None
