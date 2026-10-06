# Maryland Soccer Calendar Auditor

A review-only checker for the Maryland Soccer Calendar.

## Architecture

`Google Sheet CSV -> normalized calendar -> official schedule parser -> comparison -> Markdown report`

The public website is not changed by this tool.

## Current first-wave sources

The initial source set covers selected Maryland/DC-area programs with structured official schedules. The parser is designed for Sidearm-style schedule tables and requests the `?grid=true` representation.

## Local test

```bash
python -m pip install -r requirements.txt
pytest -q
python schedule_check.py --calendar calendar_export.csv --report audit_report.md
```

For the live published sheet:

```bash
python schedule_check.py
```

## GitHub Actions

The workflow in `.github/workflows/schedule-audit.yml` runs the checker weekly and stores the Markdown report as a workflow artifact.

The workflow is intentionally review-only. It does not commit changes to the production sheet.

## Adding a school

Add an entry to `SOURCES` in `config.py` only after:
1. the official schedule URL is confirmed;
2. the parser returns the expected number of games;
3. a few dates/times/home-away rows are spot-checked.

## Important limitation

The parser currently targets structured Sidearm tables. If a school changes platforms or the page stops exposing recognizable table rows, the run should produce a source/parser warning rather than false schedule discrepancies.
