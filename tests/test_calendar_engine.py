"""Tests for Seasonal Events calendar calculations."""

from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

from custom_components.seasonal_events.calendar_engine import (
    active_or_next_window,
    easter_sunday,
    event_windows_for_year,
    first_advent,
    hebrew_to_gregorian,
    islamic_to_gregorian,
    ramadan_windows_for_gregorian_year,
    new_year_countdown,
)
from custom_components.seasonal_events.const import (
    EVENT_CHRISTMAS_SEASON,
    EVENT_GERMAN_UNITY_DAY,
    EVENT_GUY_FAWKES_NIGHT,
    EVENT_PASSOVER,
    EVENT_RAMADAN,
    EVENT_SAUDI_NATIONAL_DAY,
    EVENT_THANKSGIVING,
    EVENT_YOM_HAATZMAUT,
)


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


def test_easter_2026() -> None:
    """Test Western Easter calculation."""
    assert easter_sunday(2026) == date(2026, 4, 5)


def test_ramadan_2026() -> None:
    """Test tabular Ramadan calculation."""
    assert islamic_to_gregorian(1447, 9, 1) == date(2026, 2, 17)
    windows = ramadan_windows_for_gregorian_year(2026)
    assert any(window.start == date(2026, 2, 17) for window in windows)


def test_hebrew_passover_2026() -> None:
    """Test Hebrew date conversion for Passover."""
    assert hebrew_to_gregorian(5786, 1, 15) == date(2026, 4, 2)
    window = active_or_next_window(EVENT_PASSOVER, date(2026, 4, 3), "de")
    assert window is not None
    assert window.contains(date(2026, 4, 3))


def test_country_specific_events_2026() -> None:
    """Test country profiles expose different country-specific events."""
    by_country = {
        country: {window.key for window in event_windows_for_year(2026, country)}
        for country in ("de", "us", "gb", "il", "sa")
    }

    assert EVENT_GERMAN_UNITY_DAY in by_country["de"]
    assert EVENT_THANKSGIVING in by_country["us"]
    assert EVENT_GUY_FAWKES_NIGHT in by_country["gb"]
    assert EVENT_YOM_HAATZMAUT in by_country["il"]
    assert EVENT_SAUDI_NATIONAL_DAY in by_country["sa"]
    assert EVENT_RAMADAN in by_country["sa"]
