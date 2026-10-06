"""Markdown audit report writer."""
from __future__ import annotations

from datetime import date

from compare import dedupe, severity
from models import Match
from normalize import display_team


def _fmt(m: Match | None) -> str:
    if not m:
        return "—"
    return f"{m.date.isoformat()} {m.time or 'TBA'} — {display_team(m.home)} vs {display_team(m.away)} ({m.status})"


def write_report(findings, source_issues, path):
    findings = dedupe(findings)
    red = [f for f in findings if severity(f["kind"], f["calendar"], f["official"]) == "RED"]
    yellow = [f for f in findings if severity(f["kind"], f["calendar"], f["official"]) == "YELLOW"]

    lines = [
        "# Maryland Soccer Calendar — Audit Report",
        "",
        f"Run date: {date.today().isoformat()}",
        "",
        "This is a review-only report. It does not modify the Google Sheet.",
        "",
        "## 🔴 ACTION NEEDED",
        "",
        "| Team | Gender | Date | Calendar | Official | Issue | Source |",
        "|---|---|---|---|---|---|---|",
    ]
    if red:
        for f in sorted(red, key=lambda x: (_fmt(x["calendar"] or x["official"]), x["team"])):
            m = f["calendar"] or f["official"]
            source = (f["official"].source_url if f["official"] else "") or ""
            lines.append(
                f"| {display_team(f['team'])} | {m.gender or '—'} | {m.date.isoformat()} | {_fmt(f['calendar'])} | "
                f"{_fmt(f['official'])} | {f['detail']} | {source} |"
            )
    else:
        lines.append("| — | — | — | — | — | None found | — |")

    lines += [
        "",
        "## 🟡 REVIEW",
        "",
        "| Team | Gender | Date | Calendar | Official | Reason | Source |",
        "|---|---|---|---|---|---|---|",
    ]
    if yellow:
        for f in sorted(yellow, key=lambda x: (_fmt(x["calendar"] or x["official"]), x["team"])):
            m = f["calendar"] or f["official"]
            source = (f["official"].source_url if f["official"] else "") or ""
            lines.append(
                f"| {display_team(f['team'])} | {m.gender or '—'} | {m.date.isoformat()} | {_fmt(f['calendar'])} | "
                f"{_fmt(f['official'])} | {f['detail']} | {source} |"
            )
    else:
        lines.append("| — | — | — | — | — | None found | — |")

    lines += ["", "## 🟢 VERIFIED", ""]
    lines.append("Sources with no discrepancies found are listed by the runner.")

    lines += ["", "## ⚠️ SOURCE / PARSER ISSUES", ""]
    if source_issues:
        for issue in source_issues:
            lines.append(f"- **{display_team(issue['team'])} ({issue['gender']})** — {issue['error']} — {issue['url']}")
    else:
        lines.append("None.")

    lines += [
        "",
        "## Notes",
        "",
        "- Findings are deduplicated at the match level.",
        "- Historical unmatched games are review items; upcoming unmatched games are action items.",
        "- Duplicate calendar entries are reported separately as action items and are grouped by gender, date, and opponent pair.",
        "- A failed fetch/parser is never treated as evidence that a game disappeared.",
        "- The auditor recommends changes; it does not make them.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
