import re
from config import TEAM_ALIASES, STATUS_ALIASES

def clean(value):
    return re.sub(r"\s+", " ", (value or "").replace("\xa0", " ")).strip()

def norm_team(value):
    raw = clean(value)
    if not raw:
        return ""
    # Remove rankings, footnote markers and common schedule decorations.
    raw = re.sub(r"^\s*(?:No\.\s*)?\d{1,2}\s*[\.\)]?\s*", "", raw, flags=re.I)
    raw = re.sub(r"[\*\u2020\u2021]+", " ", raw)
    raw = re.sub(r"\s+", " ", raw).strip()

    key = re.sub(r"[^a-z0-9]+", " ", raw.lower()).strip()
    key = re.sub(r"\s+", " ", key)

    # Exact project aliases get first priority. This matters for names such as
    # Washington College, where "College" is part of the identity.
    if key in TEAM_ALIASES:
        return TEAM_ALIASES[key]

    # Common institutional suffixes that do not identify a different opponent.
    key = re.sub(r"\b(university|college)\b", "", key)
    key = re.sub(r"\s+", " ", key).strip()

    # Common abbreviations / geographic qualifiers.
    replacements = {
        "fdu": "fdu",
        "fdu florham": "fdu",
        "fdu madison": "fdu",
        "fairleigh dickinson": "fdu",
        "fairleigh dickinson university": "fairleigh dickinson",
        "penn st": "penn state",
        "psu": "penn state",
        "washington md": "washington",
        "washington college md": "washington college",
        "st marys md": "st marys",
        "st marys college of maryland": "st marys",
        "saint marys college of maryland": "st marys",
        "mount saint mary": "mount st marys",
        "mount saint marys": "mount st marys",
        "mount st mary": "mount st marys",
        "mount st marys md": "mount st marys",
        "notre dame of maryland": "notre dame md",
        "notre dame md": "notre dame md",
        "army west point": "army",
        "army west point academy": "army",
        "james madison university": "james madison",
        "jmu": "james madison",
        "nc wesleyan": "north carolina wesleyan",
        "north carolina wesleyan university": "north carolina wesleyan",
        "alvernia": "alvernia",
        "bryn mawr": "bryn mawr",
        "hartwick": "hartwick",
        "king s": "kings",
        "kings college pa": "kings",
        "king s college pa": "kings",
        "kings college of pennsylvania": "kings",
        "gettysburg": "gettysburg",
        "bridgewater va": "bridgewater",
        "wilson college": "wilson",
        "wilson": "wilson",
        "dickinson college": "dickinson",
        "dickinson": "dickinson",
    }
    key = replacements.get(key, key)

    # Project-wide aliases.
    if key in TEAM_ALIASES:
        return TEAM_ALIASES[key]
    return key

def norm_time(value):
    raw = clean(value).lower().replace(".", "")
    if raw in {"", "-", "tba", "tb a", "time tba", "tbd", "time tbd"}:
        return None
    raw = raw.replace("noon", "12:00 pm").replace("midnight", "12:00 am")
    raw = re.sub(r"\s+", " ", raw)
    m = re.match(r"^(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$", raw)
    if not m:
        return clean(value)
    hour = int(m.group(1))
    minute = int(m.group(2) or 0)
    ap = m.group(3)
    if ap:
        if ap == "pm" and hour != 12:
            hour += 12
        if ap == "am" and hour == 12:
            hour = 0
    return f"{hour:02d}:{minute:02d}"

def norm_status(value):
    raw = clean(value).lower()
    if raw in {"", "-", "—", "–", "scheduled", "upcoming", "not started", "preview"}:
        return "Scheduled"
    key = re.sub(r"[^a-z]+", " ", raw).strip()
    return STATUS_ALIASES.get(key, clean(value))
