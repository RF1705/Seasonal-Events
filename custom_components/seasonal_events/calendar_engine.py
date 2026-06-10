"""Calendar calculations for Seasonal Events."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from .const import (
    EVENT_ADVENT,
    EVENT_ASHURA,
    EVENT_CHRISTMAS_SEASON,
    EVENT_EASTER,
    EVENT_EID_AL_ADHA,
    EVENT_EID_AL_FITR,
    EVENT_GERMAN_UNITY_DAY,
    EVENT_GUY_FAWKES_NIGHT,
    EVENT_HALLOWEEN,
    EVENT_HANUKKAH,
    EVENT_LAILAT_AL_QADR,
    EVENT_NEW_YEAR,
    EVENT_PASSOVER,
    EVENT_PURIM,
    EVENT_RAMADAN,
    EVENT_ROSH_HASHANAH,
    EVENT_SAUDI_NATIONAL_DAY,
    EVENT_SHAVUOT,
    EVENT_SUKKOT,
    EVENT_THANKSGIVING,
    EVENT_YOM_HAATZMAUT,
    EVENT_YOM_KIPPUR,
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


def nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> date:
    """Return the nth weekday of a month."""
    current = date(year, month, 1)
    offset = (weekday - current.weekday()) % 7
    return current + timedelta(days=offset + 7 * (n - 1))


def hebrew_leap_year(year: int) -> bool:
    """Return true if the Hebrew year is a leap year."""
    return ((7 * year + 1) % 19) < 7


def _hebrew_calendar_elapsed_days(year: int) -> int:
    """Return days elapsed until Hebrew year starts."""
    months_elapsed = (
        235 * ((year - 1) // 19)
        + 12 * ((year - 1) % 19)
        + ((7 * ((year - 1) % 19) + 1) // 19)
    )
    parts_elapsed = 204 + 793 * (months_elapsed % 1080)
    hours_elapsed = (
        5
        + 12 * months_elapsed
        + 793 * (months_elapsed // 1080)
        + parts_elapsed // 1080
    )
    day = 1 + 29 * months_elapsed + hours_elapsed // 24
    parts = 1080 * (hours_elapsed % 24) + parts_elapsed % 1080

    if (
        parts >= 19440
        or (day % 7 == 2 and parts >= 9924 and not hebrew_leap_year(year))
        or (day % 7 == 1 and parts >= 16789 and hebrew_leap_year(year - 1))
    ):
        day += 1

    if day % 7 in (0, 3, 5):
        day += 1

    return day


def hebrew_year_days(year: int) -> int:
    """Return the number of days in a Hebrew year."""
    return _hebrew_calendar_elapsed_days(year + 1) - _hebrew_calendar_elapsed_days(year)


def hebrew_month_days(year: int, month: int) -> int:
    """Return the number of days in a Hebrew month."""
    if month in (2, 4, 6, 10, 13):
        return 29
    if month == 12 and not hebrew_leap_year(year):
        return 29
    if month == 8 and hebrew_year_days(year) % 10 != 5:
        return 29
    if month == 9 and hebrew_year_days(year) % 10 == 3:
        return 29
    return 30


def hebrew_to_absolute(year: int, month: int, day: int) -> int:
    """Convert a Hebrew date to an absolute day number."""
    days = day
    if month < 7:
        final_month = 13 if hebrew_leap_year(year) else 12
        for current_month in range(7, final_month + 1):
            days += hebrew_month_days(year, current_month)
        for current_month in range(1, month):
            days += hebrew_month_days(year, current_month)
    else:
        for current_month in range(7, month):
            days += hebrew_month_days(year, current_month)

    return days + _hebrew_calendar_elapsed_days(year) - 1373429


def hebrew_to_gregorian(year: int, month: int, day: int) -> date:
    """Convert a Hebrew date to Gregorian date."""
    return date.fromordinal(hebrew_to_absolute(year, month, day))


def hebrew_years_for_gregorian_year(year: int) -> range:
    """Return Hebrew years that can overlap a Gregorian year."""
    return range(year + 3759, year + 3762)


def _islamic_to_julian_day(year: int, month: int, day: int) -> int:
    """Return Julian day number for a tabular Islamic date."""
    return (
        day
        + int((29.5 * (month - 1)) + 0.999999)
        + (year - 1) * 354
        + ((3 + (11 * year)) // 30)
        + 1948439
        - 1
    )


def _julian_day_to_gregorian(julian_day: int) -> date:
    """Convert Julian day number to Gregorian date."""
    a = julian_day + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + (m // 10)
    return date(year, month, day)


def islamic_to_gregorian(year: int, month: int, day: int) -> date:
    """Convert a tabular Islamic date to Gregorian date."""
    return _julian_day_to_gregorian(_islamic_to_julian_day(year, month, day))


def ramadan_windows_for_gregorian_year(year: int) -> list[EventWindow]:
    """Return Ramadan windows overlapping a Gregorian year."""
    # A Gregorian year overlaps one or sometimes two Islamic years.
    islamic_year_estimate = int(((year - 622) * 33) / 32)
    windows: list[EventWindow] = []

    for islamic_year in range(islamic_year_estimate - 1, islamic_year_estimate + 3):
        start = islamic_to_gregorian(islamic_year, 9, 1)
        end = islamic_to_gregorian(islamic_year, 9, 30)
        if start.year <= year <= end.year or start.year == year or end.year == year:
            windows.append(
                EventWindow(
                    key=EVENT_RAMADAN,
                    name="Ramadan",
                    start=start,
                    end=end,
                    icon="mdi:moon-waxing-crescent",
                )
            )

    return windows


def islamic_windows_for_gregorian_year(
    year: int,
    event_key: str,
    name: str,
    month: int,
    start_day: int,
    end_day: int,
    icon: str,
) -> list[EventWindow]:
    """Return Islamic event windows overlapping a Gregorian year."""
    islamic_year_estimate = int(((year - 622) * 33) / 32)
    windows: list[EventWindow] = []

    for islamic_year in range(islamic_year_estimate - 1, islamic_year_estimate + 3):
        start = islamic_to_gregorian(islamic_year, month, start_day)
        end = islamic_to_gregorian(islamic_year, month, end_day)
        if start.year <= year <= end.year or start.year == year or end.year == year:
            windows.append(
                EventWindow(
                    key=event_key,
                    name=name,
                    start=start,
                    end=end,
                    icon=icon,
                )
            )

    return windows


def jewish_windows_for_gregorian_year(year: int, diaspora: bool) -> list[EventWindow]:
    """Return Jewish event windows overlapping a Gregorian year."""
    windows: list[EventWindow] = []

    for hebrew_year in hebrew_years_for_gregorian_year(year):
        purim_month = 13 if hebrew_leap_year(hebrew_year) else 12
        events = [
            (
                EVENT_ROSH_HASHANAH,
                "Rosh Hashanah",
                7,
                1,
                2,
                "mdi:calendar-star",
            ),
            (
                EVENT_YOM_KIPPUR,
                "Yom Kippur",
                7,
                10,
                10,
                "mdi:star-david",
            ),
            (
                EVENT_SUKKOT,
                "Sukkot",
                7,
                15,
                21 if not diaspora else 22,
                "mdi:palm-tree",
            ),
            (
                EVENT_HANUKKAH,
                "Hanukkah",
                9,
                25,
                25,
                "mdi:menorah",
            ),
            (
                EVENT_PASSOVER,
                "Passover",
                1,
                15,
                21 if not diaspora else 22,
                "mdi:matzah",
            ),
            (
                EVENT_SHAVUOT,
                "Shavuot",
                3,
                6,
                6 if not diaspora else 7,
                "mdi:book-open-page-variant",
            ),
            (
                EVENT_PURIM,
                "Purim",
                purim_month,
                14,
                14,
                "mdi:party-popper",
            ),
        ]

        for event_key, name, month, start_day, end_day, icon in events:
            start = hebrew_to_gregorian(hebrew_year, month, start_day)
            if event_key == EVENT_HANUKKAH:
                end = start + timedelta(days=7)
            else:
                end = hebrew_to_gregorian(hebrew_year, month, end_day)
            if start.year <= year <= end.year or start.year == year or end.year == year:
                windows.append(EventWindow(event_key, name, start, end, icon))

    return windows


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
    if region_profile not in {"de", "us", "gb", "il", "sa"}:
        region_profile = "de"

    easter = easter_sunday(year)
    diaspora = region_profile != "il"

    windows = [
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
    if region_profile == "de":
        windows.append(
            EventWindow(
                key=EVENT_GERMAN_UNITY_DAY,
                name="German Unity Day",
                start=date(year, 10, 3),
                end=date(year, 10, 3),
                icon="mdi:flag",
            )
        )
    if region_profile == "us":
        thanksgiving = nth_weekday_of_month(year, 11, 3, 4)
        windows.append(
            EventWindow(
                key=EVENT_THANKSGIVING,
                name="Thanksgiving",
                start=thanksgiving,
                end=thanksgiving,
                icon="mdi:turkey",
            )
        )
    if region_profile == "gb":
        windows.append(
            EventWindow(
                key=EVENT_GUY_FAWKES_NIGHT,
                name="Guy Fawkes Night",
                start=date(year, 11, 5),
                end=date(year, 11, 5),
                icon="mdi:firework",
            )
        )
    if region_profile == "il":
        # Common civil observance date. Formal postponement rules can be added
        # once country-specific holiday rules are introduced.
        windows.append(
            EventWindow(
                key=EVENT_YOM_HAATZMAUT,
                name="Yom Ha'atzmaut",
                start=hebrew_to_gregorian(year + 3760, 2, 5),
                end=hebrew_to_gregorian(year + 3760, 2, 5),
                icon="mdi:flag-star",
            )
        )
    if region_profile == "sa":
        windows.append(
            EventWindow(
                key=EVENT_SAUDI_NATIONAL_DAY,
                name="Saudi National Day",
                start=date(year, 9, 23),
                end=date(year, 9, 23),
                icon="mdi:flag",
            )
        )

    windows.extend(ramadan_windows_for_gregorian_year(year))
    windows.extend(
        islamic_windows_for_gregorian_year(
            year,
            EVENT_EID_AL_FITR,
            "Eid al-Fitr",
            10,
            1,
            3,
            "mdi:moon-waxing-crescent",
        )
    )
    windows.extend(
        islamic_windows_for_gregorian_year(
            year,
            EVENT_EID_AL_ADHA,
            "Eid al-Adha",
            12,
            10,
            13,
            "mdi:sheep",
        )
    )
    windows.extend(
        islamic_windows_for_gregorian_year(
            year,
            EVENT_ASHURA,
            "Ashura",
            1,
            10,
            10,
            "mdi:calendar-star",
        )
    )
    windows.extend(
        islamic_windows_for_gregorian_year(
            year,
            EVENT_LAILAT_AL_QADR,
            "Lailat al-Qadr",
            9,
            27,
            27,
            "mdi:star-crescent",
        )
    )
    windows.extend(jewish_windows_for_gregorian_year(year, diaspora))
    return windows


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
