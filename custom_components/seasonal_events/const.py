"""Constants for Seasonal Events."""

from __future__ import annotations

DOMAIN = "seasonal_events"

CONF_REGION_PROFILE = "region_profile"
CONF_ENABLED_EVENTS = "enabled_events"

DEFAULT_REGION_PROFILE = "western_christian"

EVENT_ADVENT = "advent"
EVENT_CHRISTMAS_SEASON = "christmas_season"
EVENT_NEW_YEAR = "new_year"
EVENT_HALLOWEEN = "halloween"

DEFAULT_EVENTS = [
    EVENT_ADVENT,
    EVENT_CHRISTMAS_SEASON,
    EVENT_NEW_YEAR,
    EVENT_HALLOWEEN,
]

REGION_PROFILES = {
    "western_christian": "Western Christian",
}
