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
    # Normalize common abbreviations before punctuation cleanup.
    s = re.sub(r"\buniv\.?\b", "university", s)
    s = re.sub(r"\bu\.?\b", "university", s)
    s = re.sub(r"\bcol\.?\b", "college", s)
    # Normalize punctuation while preserving words.
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm_team(value: str | None) -> str:
    raw = clean(value)
    key = _team_key(raw)
    if not key:
        return ""

    # Exact configured aliases get first priority. This is important for names
    # such as Washington College, where "College" is part of the identity.
    if key in TEAM_ALIASES:
        return TEAM_ALIASES[key]

    # Remove state/location parentheticals after exact aliases have had a chance
    # to match (e.g. "Bridgewater (Va.)", "Mount St. Mary's (Md.)").
    key = re.sub(
        r"\s+(?:md|pa|va|dc|nj|ny|de|ma|ct|ri|nc|sc|wv|oh|mi|il|in|wi|mn|ky|tn|al|ga|tx|ca|az|ar|co|or|wa)$",
        "",
        key,
    )

    # Common academic suffixes generally do not identify a different opponent.
    key = re.sub(r"\s+(?:university|college|school)$", "", key)

    if key in TEAM_ALIASES:
        return TEAM_ALIASES[key]

    # Common "University of ..." pattern.
    if key.startswith("university of "):
        shortened = key[len("university of "): ]
        if shortened in TEAM_ALIASES:
            return TEAM_ALIASES[shortened]

    return key


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


def display_team(value: str | None) -> str:
    """Return the canonical human-readable team name for audit reports."""
    raw = clean(value)
    if not raw:
        return ""

    # Always route display names through the same alias normalization used for
    # matching. This prevents report-only forms such as "Mcdaniel" or
    # "Notre Dame (md)" from leaking through.
    canonical = norm_team(raw)
    if canonical:
        # Known aliases are already presentation-ready. Unknown names get a
        # conservative title-case cleanup for report readability.
        if canonical == raw.lower():
            acronyms = {"nc": "NC", "pa": "PA", "va": "VA", "md": "MD", "dc": "DC", "fdu": "FDU", "umass": "UMass"}
            return " ".join(acronyms.get(w.lower(), w.capitalize()) for w in canonical.split())
        return canonical
    return raw
