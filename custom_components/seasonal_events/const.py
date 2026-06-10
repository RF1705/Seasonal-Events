"""Constants for Seasonal Events."""

from __future__ import annotations

DOMAIN = "seasonal_events"

CONF_NAME = "name"
CONF_COUNTRY_PROFILE = "country_profile"
CONF_REGION_PROFILE = "region_profile"
CONF_ENABLED_EVENTS = "enabled_events"
CONF_EVENT_COLLECTIONS = "event_collections"

DEFAULT_NAME = "Deutschland"
DEFAULT_COUNTRY_PROFILE = "de"
DEFAULT_REGION_PROFILE = DEFAULT_COUNTRY_PROFILE

COLLECTION_CULTURAL = "cultural"
COLLECTION_CHRISTIAN_CULTURAL = "christian_cultural"

EVENT_ADVENT = "advent"
EVENT_CHRISTMAS_SEASON = "christmas_season"
EVENT_NEW_YEAR = "new_year"
EVENT_HALLOWEEN = "halloween"
EVENT_EASTER = "easter"

DEFAULT_EVENTS = [
    EVENT_NEW_YEAR,
    EVENT_HALLOWEEN,
    EVENT_CHRISTMAS_SEASON,
    EVENT_EASTER,
]

DEFAULT_EVENT_COLLECTIONS = [
    COLLECTION_CULTURAL,
    COLLECTION_CHRISTIAN_CULTURAL,
]

COUNTRY_PROFILES = {
    "de": "Deutschland",
}

REGION_PROFILES = COUNTRY_PROFILES

EVENTS = {
    EVENT_NEW_YEAR: {
        "name": "New Year",
        "collection": COLLECTION_CULTURAL,
    },
    EVENT_HALLOWEEN: {
        "name": "Halloween",
        "collection": COLLECTION_CULTURAL,
    },
    EVENT_ADVENT: {
        "name": "Advent",
        "collection": COLLECTION_CHRISTIAN_CULTURAL,
    },
    EVENT_CHRISTMAS_SEASON: {
        "name": "Christmas Season",
        "collection": COLLECTION_CHRISTIAN_CULTURAL,
    },
    EVENT_EASTER: {
        "name": "Easter",
        "collection": COLLECTION_CHRISTIAN_CULTURAL,
    },
}

EVENT_COLLECTIONS = {
    COLLECTION_CULTURAL: "Allgemein / kulturell",
    COLLECTION_CHRISTIAN_CULTURAL: "Christlich / kulturell",
}
