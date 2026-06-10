"""Tests for Seasonal Events calendar calculations."""

from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

from custom_components.seasonal_events.calendar_engine import (
    active_or_next_window,
    first_advent,
    new_year_countdown,
)
from custom_components.seasonal_events.const import EVENT_CHRISTMAS_SEASON


def test_first_advent_2026() -> None:
    """Test first Advent calculation."""
    assert first_advent(2026) == date(2026, 11, 29)


def test_christmas_season_crosses_year_boundary() -> None:
    """Test Christmas season remains active in January."""
    window = active_or_next_window(
        EVENT_CHRISTMAS_SEASON,
        date(2027, 1, 6),
        "western_christian",
    )

    assert window is not None
    assert window.contains(date(2027, 1, 6))
    assert window.start == date(2026, 11, 29)
    assert window.end == date(2027, 1, 6)


def test_new_year_countdown() -> None:
    """Test New Year countdown values."""
    countdown = new_year_countdown(
        datetime(2026, 12, 31, 23, 59, 30, tzinfo=ZoneInfo("Europe/Berlin"))
    )

    assert countdown["total_seconds"] == 30
    assert countdown["formatted"] == "0d 00:00:30"
