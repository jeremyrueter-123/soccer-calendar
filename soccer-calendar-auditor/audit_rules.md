# Audit rules

The auditor is a review tool, not an automatic editor.

## Match identity
A match is identified primarily by:
- gender
- team
- opponent
- approximate date window

## Compare
For a matched game, compare:
- date
- time
- home/away
- status

## Flag levels
RED = strong evidence of a calendar change/error
- official cancellation/no contest/postponement
- official date differs
- official time differs
- official home/away differs
- calendar game absent from official schedule when the source is reliable

YELLOW = review
- parser/source ambiguity
- TBA versus a specific time when identity is otherwise uncertain
- newly appearing official game that cannot yet be confidently matched

GREEN = match
- identity, date, time, home/away and status agree

## Windows
Upcoming window:
- all included future games

Recent window:
- recently completed games, used primarily for status changes

## Deduplication
The same discrepancy can appear from both teams.
Collapse it to one calendar-level finding before reporting.

## Never
- Never edit the Google Sheet automatically.
- Never treat a failed web fetch as evidence that a game disappeared.
- Never report a parser failure as a schedule discrepancy.
