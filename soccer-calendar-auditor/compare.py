from datetime import timedelta
from dataclasses import dataclass
from normalize import norm_team, norm_time, norm_status
from models import Match

@dataclass
class Finding:
    severity: str
    team: str
    calendar: Match | None
    official: Match | None
    issue: str

def _opp(m, team):
    return norm_team(m.away if norm_team(m.home) == norm_team(team) else m.home)

def _same_pair(a, b, team):
    return _opp(a, team) == _opp(b, team)

def dedupe(matches):
    """Collapse exact calendar duplicates, preserving the most informative time/status."""
    groups = {}
    for m in matches:
        key = (m.date, tuple(sorted((norm_team(m.home), norm_team(m.away)))),
               m.gender, norm_status(m.status))
        groups.setdefault(key, []).append(m)

    out = []
    for group in groups.values():
        if len(group) == 1:
            out.append(group[0])
            continue
        # Prefer a concrete time over TBA.
        chosen = next((m for m in group if norm_time(m.time)), group[0])
        out.append(chosen)
    return out

def duplicate_findings(calendar):
    findings = []
    seen = {}
    for m in calendar:
        key = (m.date, tuple(sorted((norm_team(m.home), norm_team(m.away)))), m.gender)
        seen.setdefault(key, []).append(m)
    for group in seen.values():
        if len(group) > 1:
            first = group[0]
            times = ", ".join(norm_time(m.time) or "TBA" for m in group)
            findings.append(Finding(
                "RED", first.source_team, first, None,
                f"Duplicate calendar entries ({times})"
            ))
    return findings

def compare(calendar, official, team, today):
    findings = []
    cal = [m for m in calendar if m.source_team == team]
    off = [m for m in official if m.source_team == team]
    used = set()

    for cm in cal:
        exact = next((i for i, om in enumerate(off)
                      if i not in used and om.date == cm.date and _same_pair(cm, om, team)), None)
        if exact is not None:
            om = off[exact]; used.add(exact)

            if cm.date != om.date:
                continue

            # Past matches: existence/status are important; time/home-away are not.
            if cm.date < today:
                if norm_status(cm.status) != norm_status(om.status):
                    findings.append(Finding("RED", team, cm, om, "Match status differs"))
                continue

            if norm_time(cm.time) != norm_time(om.time):
                # TBA -> a real time is a legitimate upcoming change.
                if not (norm_time(cm.time) is None and norm_time(om.time) is None):
                    findings.append(Finding("RED", team, cm, om, "Kickoff time differs"))

            if norm_team(cm.home) != norm_team(om.home) or norm_team(cm.away) != norm_team(om.away):
                findings.append(Finding("RED", team, cm, om, "Home/away designation differs"))

            if norm_status(cm.status) != norm_status(om.status):
                findings.append(Finding("RED", team, cm, om, "Match status differs"))
            continue

        # Look for a date move of the same opponent within +/- 14 days.
        moved = next((om for i, om in enumerate(off) if i not in used and
                      _same_pair(cm, om, team) and
                      abs((om.date - cm.date).days) <= 14), None)
        if moved:
            idx = off.index(moved); used.add(idx)
            sev = "RED" if cm.date >= today else "YELLOW"
            findings.append(Finding(sev, team, cm, moved,
                                    f"Date differs by {(moved.date - cm.date).days} day(s)"))
        else:
            sev = "RED" if cm.date >= today else "YELLOW"
            findings.append(Finding(sev, team, cm, None, "Calendar game not found on official schedule"))

    for i, om in enumerate(off):
        if i in used:
            continue
        sev = "RED" if om.date >= today else "YELLOW"
        findings.append(Finding(sev, team, None, om, "Official schedule has an unmatched game"))

    return findings
