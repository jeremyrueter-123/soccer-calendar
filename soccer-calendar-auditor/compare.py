"""Review-only comparison engine."""
from __future__ import annotations

from datetime import date

from models import Match
from normalize import norm_team, norm_time


def _opponent(m: Match, team: str) -> str:
    return norm_team(m.away) if norm_team(m.home) == team else norm_team(m.home)


def _same_identity(a: Match, b: Match, team: str) -> bool:
    return _opponent(a, team) == _opponent(b, team)


def _finding(kind, team, calendar=None, official=None, detail=""):
    return {
        "kind": kind,
        "team": team,
        "calendar": calendar,
        "official": official,
        "detail": detail,
    }


def compare_team(calendar: list[Match], official: list[Match], team: str, gender: str | None = None):
    team = norm_team(team)
    cal = [
        m for m in calendar
        if team in {norm_team(m.home), norm_team(m.away)}
        and (gender is None or not m.gender or m.gender.lower() == gender.lower())
    ]
    off = [
        m for m in official
        if team in {norm_team(m.home), norm_team(m.away)}
        and (gender is None or not m.gender or m.gender.lower() == gender.lower())
    ]

    used: set[int] = set()
    findings = []

    # Exact identity/date first.
    for c in cal:
        exact = [
            (i, o) for i, o in enumerate(off)
            if i not in used and o.date == c.date and _same_identity(c, o, team)
        ]
        if exact:
            i, o = exact[0]
            used.add(i)
            if norm_time(c.time) != norm_time(o.time) and o.time is not None:
                findings.append(_finding("TIME", team, c, o, "Kickoff time differs"))
            if (norm_team(c.home), norm_team(c.away)) != (norm_team(o.home), norm_team(o.away)):
                findings.append(_finding("HOME_AWAY", team, c, o, "Home/away designation differs"))
            if c.status != o.status:
                findings.append(_finding("STATUS", team, c, o, "Match status differs"))
            continue

        # Date-move match: same team/opponent within +/-14 days.
        near = []
        for i, o in enumerate(off):
            if i in used or not _same_identity(c, o, team):
                continue
            delta = abs((c.date - o.date).days)
            if delta <= 14:
                near.append((delta, i, o))
        if near:
            delta, i, o = sorted(near)[0]
            used.add(i)
            findings.append(_finding("DATE", team, c, o, f"Date differs by {delta} day(s)"))
            if norm_time(c.time) != norm_time(o.time) and o.time is not None:
                findings.append(_finding("TIME", team, c, o, "Kickoff time differs"))
            if (norm_team(c.home), norm_team(c.away)) != (norm_team(o.home), norm_team(o.away)):
                findings.append(_finding("HOME_AWAY", team, c, o, "Home/away designation differs"))
            if c.status != o.status:
                findings.append(_finding("STATUS", team, c, o, "Match status differs"))
        else:
            findings.append(_finding("MISSING_OFFICIAL", team, c, None, "Calendar game not found on official schedule"))

    # Official games not represented in the calendar.
    for i, o in enumerate(off):
        if i not in used:
            findings.append(_finding("NEW_OFFICIAL", team, None, o, "Official schedule has an unmatched game"))

    return findings


def severity(kind: str, calendar: Match | None, official: Match | None) -> str:
    if kind in {"DATE", "TIME", "HOME_AWAY", "STATUS", "MISSING_OFFICIAL"}:
        return "RED"
    if kind == "NEW_OFFICIAL":
        return "YELLOW"
    return "YELLOW"


def dedupe(findings):
    """Collapse team-side duplicates into one match-level finding."""
    result = {}
    for f in findings:
        c, o = f["calendar"], f["official"]
        if c:
            key = ("calendar", c.gender, c.date, frozenset((c.home, c.away)), f["kind"])
        elif o:
            key = ("official", o.gender, o.date, frozenset((o.home, o.away)), f["kind"])
        else:
            key = ("unknown", f["team"], f["kind"], f["detail"])
        result[key] = f
    return list(result.values())
