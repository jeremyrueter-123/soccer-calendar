# Maryland Soccer Calendar Auditor

A review-only checker for the Maryland Soccer Calendar.

## Scope

The auditor covers the established Maryland college soccer scope:

- Maryland — men/women
- UMBC — men/women
- Mount St. Mary's — men/women
- Loyola Maryland — men/women
- Navy — men/women
- Towson — women
- Frostburg State — men/women
- Goucher — men/women
- Hood — men/women
- Johns Hopkins — men/women
- McDaniel — men/women
- Notre Dame of Maryland — men/women
- Salisbury — men/women
- St. Mary's College of Maryland — men/women
- Stevenson — men/women
- Washington College — men/women

Catholic University is intentionally excluded because it is in Washington, D.C.

## Architecture

`Google Sheet CSV -> normalized calendar -> official schedule parser -> comparison -> Markdown report`

The public website is not changed by this tool.

## What the auditor checks

For upcoming games it checks:

- date changes
- kickoff-time changes
- home/away changes
- cancellations and other status changes
- games appearing on an official schedule but not in the calendar
- calendar games missing from the official schedule
- duplicate calendar entries

For historical games, the audit intentionally avoids noisy kickoff-time and home/away discrepancies and focuses on game existence/date and status.

Historical unmatched games are **Review** items. Upcoming unmatched games are **Action Needed** items.

## v9 improvements

- Treats `-`, `—`, and similar pre-result markers as `Scheduled`.
- Handles common `University` / `College` suffixes without confusing distinct teams.
- Handles common state suffixes such as `(Md.)`, `(Va.)`, and `(Pa.)`.
- Handles common opponent abbreviations including FDU/Fairleigh Dickinson and Army/Army West Point.
- Keeps common team identities such as Washington College, St. John's, and Mount St. Mary's intact.
- Explicitly detects duplicate calendar rows for the same gender, date, and opponent pair.
- Includes gender in the audit tables so simultaneous men's and women's matches are not mistaken for duplicates.
- Cleans report names such as `st mary s`, `notre dame`, and lowercase opponent names without changing match identity.
- Preserves home/away discrepancies as actionable findings; the official schedule remains the comparison authority.

## Important source limitation

Goucher's current athletics schedule endpoint returns HTTP 405 to the checker. The auditor reports that as a source/parser issue rather than treating it as evidence that games disappeared.

## Local test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python schedule_check.py --calendar calendar_export.csv --report audit_report.md
```

For the live published sheet:

```bash
python schedule_check.py
```

## GitHub Actions

The workflow in `.github/workflows/schedule-audit.yml` runs the checker weekly and stores the Markdown report as a workflow artifact. It can also be run manually from the Actions tab.

The workflow is intentionally review-only. It does not commit changes to the production sheet.

## Adding or changing a source

Add or update an entry in `SOURCES` in `config.py` only after:
1. the official schedule URL is confirmed;
2. the parser returns recognizable schedule rows;
3. a few dates/times/home-away rows are spot-checked.

If a school changes platforms or the page stops exposing recognizable rows, the run should produce a source/parser warning rather than false schedule discrepancies.
