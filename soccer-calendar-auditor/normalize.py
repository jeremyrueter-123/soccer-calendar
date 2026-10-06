"""Normalization helpers shared by calendar and official parsers."""
from __future__ import annotations

import re
from datetime import date, datetime

from config import STATUS_ALIASES, TEAM_ALIASES


def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", (value or "").replace("\xa0", " ")).strip()


def norm_team(value: str | None) -> str:
    raw = clean(value)
    key = re.sub(r"[^a-z0-9 ]+", "", raw.lower())
    key = re.sub(r"\s+", " ", key).strip()
    return TEAM_ALIASES.get(key, raw)


def norm_time(value: str | None) -> str | None:
    s = clean(value).lower().replace(".", "")
    if not s or s in {"tba", "tbd", "-", "—", "n/a"}:
        return None
    s = re.sub(r"\s+et$", "", s)
    m = re.match(r"^(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$", s)
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

    # Sidearm often gives strings such as "Aug 20 (Thu)" or "Oct 24".
    m = re.match(r"^([A-Za-z]+)\s+(\d{1,2})", s)
    if m:
        for fmt in ("%b %d", "%B %d"):
            try:
                d = datetime.strptime(f"{year} {m.group(1)} {m.group(2)}", f"%Y {fmt}").date()
                return d
            except ValueError:
                pass
    return None
