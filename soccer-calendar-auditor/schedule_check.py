#!/usr/bin/env python3
"""Run the Maryland Soccer Calendar schedule audit."""
from __future__ import annotations

import argparse
from pathlib import Path

from calendar_loader import load_calendar
from compare import compare_team, dedupe, find_calendar_duplicates
from config import CALENDAR_CSV_URL, SOURCES
from parser import parse_source
from report import write_report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calendar", default=CALENDAR_CSV_URL,
                    help="Local CSV path or published Google Sheets CSV URL")
    ap.add_argument("--report", default="audit_report.md")
    args = ap.parse_args()

    calendar = load_calendar(args.calendar)
    print(f"Loaded {len(calendar)} included calendar matches.")

    findings = find_calendar_duplicates(calendar)
    source_issues = []
    verified = []

    for source in SOURCES:
        print(f"Checking {source['team']} ({source['gender']})...")
        result = parse_source(source)
        if result.error:
            source_issues.append({
                "team": source["team"], "gender": source["gender"],
                "url": source["url"], "error": result.error
            })
            continue

        team_findings = compare_team(
            calendar, result.matches, source["team"], source["gender"]
        )
        findings.extend(team_findings)
        if not team_findings:
            verified.append(f"{source['team']} ({source['gender']})")

    findings = dedupe(findings)

    report_path = Path(args.report)
    write_report(findings, source_issues, report_path)

    print(f"Report written to {report_path}")
    print(f"Findings: {len(findings)}")
    print(f"Verified sources: {len(verified)}")
    print(f"Source/parser issues: {len(source_issues)}")


if __name__ == "__main__":
    main()
