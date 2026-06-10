"""Data models for Seasonal Events."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class EventWindow:
    """A yearly seasonal event window."""

    key: str
    name: str
    start: date
    end: date
    icon: str

    def contains(self, today: date) -> bool:
        """Return true if today is inside the event window."""
        return self.start <= today <= self.end

    def days_until_start(self, today: date) -> int:
        """Return days until the event starts."""
        return max((self.start - today).days, 0)

    def days_until_end(self, today: date) -> int:
        """Return days until the event ends."""
        return max((self.end - today).days, 0)
