"""Calendar calculations for Seasonal Events."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from .const import (
    EVENT_ADVENT,
    EVENT_CHRISTMAS_SEASON,
    EVENT_EASTER,
    EVENT_HALLOWEEN,
    EVENT_NEW_YEAR,
)
from .models import EventWindow


def first_advent(year: int) -> date:
    """Return the first Advent Sunday for the given year."""
    christmas_eve = date(year, 12, 24)
    days_since_sunday = (christmas_eve.weekday() + 1) % 7
    fourth_advent = christmas_eve - timedelta(days=days_since_sunday)
    return fourth_advent - timedelta(days=21)


def easter_sunday(year: int) -> date:
    """Return Western Easter Sunday for the given year."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def next_new_year(now: datetime) -> datetime:
    """Return the next local New Year midnight."""
    target_year = now.year + 1
    return datetime.combine(
        date(target_year, 1, 1),
        time.min,
        tzinfo=now.tzinfo,
    )


def new_year_countdown(now: datetime) -> dict[str, int | str]:
    """Return a countdown to the next New Year."""
    target = next_new_year(now)
    remaining_seconds = max(int((target - now).total_seconds()), 0)
    days, remainder = divmod(remaining_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return {
        "target": target.isoformat(),
        "total_seconds": remaining_seconds,
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "formatted": f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}",
    }


def event_windows_for_year(year: int, region_profile: str) -> list[EventWindow]:
    """Return event windows for a year and region profile."""
    if region_profile == "western_christian":
        region_profile = "de"
    if region_profile != "de":
        region_profile = "de"

    easter = easter_sunday(year)

    return [
        EventWindow(
            key=EVENT_ADVENT,
            name="Advent",
            start=first_advent(year),
            end=date(year, 12, 24),
            icon="mdi:candle",
        ),
        EventWindow(
            key=EVENT_CHRISTMAS_SEASON,
            name="Christmas Season",
            start=first_advent(year),
            end=date(year + 1, 1, 6),
            icon="mdi:string-lights",
        ),
        EventWindow(
            key=EVENT_NEW_YEAR,
            name="New Year",
            start=date(year, 12, 31),
            end=date(year + 1, 1, 1),
            icon="mdi:party-popper",
        ),
        EventWindow(
            key=EVENT_HALLOWEEN,
            name="Halloween",
            start=date(year, 10, 31),
            end=date(year, 10, 31),
            icon="mdi:pumpkin",
        ),
        EventWindow(
            key=EVENT_EASTER,
            name="Easter",
            start=easter - timedelta(days=2),
            end=easter + timedelta(days=1),
            icon="mdi:egg-easter",
        ),
    ]


def active_or_next_window(
    event_key: str,
    today: date,
    region_profile: str,
) -> EventWindow | None:
    """Return the currently active or next upcoming window for an event."""
    windows = [
        window
        for year in (today.year - 1, today.year, today.year + 1)
        for window in event_windows_for_year(year, region_profile)
        if window.key == event_key
    ]
    windows.sort(key=lambda window: window.start)

    for window in windows:
        if window.contains(today):
            return window

    for window in windows:
        if window.start > today:
            return window

    return None


def local_now(time_zone: str) -> datetime:
    """Return timezone-aware now for tests and entities."""
    return datetime.now(ZoneInfo(time_zone))
