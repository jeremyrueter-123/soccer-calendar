"""Shared normalized records."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Match:
    date: date
    time: str | None
    home: str
    away: str
    status: str = "Scheduled"
    gender: str | None = None
    source_team: str | None = None
    source_url: str | None = None

    @property
    def opponent(self) -> str:
        return self.away if self.home == self.source_team else self.home
