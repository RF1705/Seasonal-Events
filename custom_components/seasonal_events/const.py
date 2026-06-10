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
COLLECTION_ISLAMIC_CULTURAL = "islamic_cultural"

EVENT_ADVENT = "advent"
EVENT_CHRISTMAS_SEASON = "christmas_season"
EVENT_NEW_YEAR = "new_year"
EVENT_HALLOWEEN = "halloween"
EVENT_EASTER = "easter"
EVENT_RAMADAN = "ramadan"

DEFAULT_EVENTS = [
    EVENT_NEW_YEAR,
    EVENT_HALLOWEEN,
    EVENT_CHRISTMAS_SEASON,
    EVENT_EASTER,
    EVENT_RAMADAN,
]

DEFAULT_EVENT_COLLECTIONS = [
    COLLECTION_CULTURAL,
    COLLECTION_CHRISTIAN_CULTURAL,
    COLLECTION_ISLAMIC_CULTURAL,
]

COUNTRY_PROFILES = {
    "de": "Deutschland",
}

REGION_PROFILES = COUNTRY_PROFILES

EVENTS = {
    EVENT_NEW_YEAR: {
        "translation_key": "new_year",
        "collection": COLLECTION_CULTURAL,
    },
    EVENT_HALLOWEEN: {
        "translation_key": "halloween",
        "collection": COLLECTION_CULTURAL,
    },
    EVENT_ADVENT: {
        "translation_key": "advent",
        "collection": COLLECTION_CHRISTIAN_CULTURAL,
    },
    EVENT_CHRISTMAS_SEASON: {
        "translation_key": "christmas_season",
        "collection": COLLECTION_CHRISTIAN_CULTURAL,
    },
    EVENT_EASTER: {
        "translation_key": "easter",
        "collection": COLLECTION_CHRISTIAN_CULTURAL,
    },
    EVENT_RAMADAN: {
        "translation_key": "ramadan",
        "collection": COLLECTION_ISLAMIC_CULTURAL,
    },
}

EVENT_COLLECTIONS = {
    COLLECTION_CULTURAL: "Allgemein / kulturell",
    COLLECTION_CHRISTIAN_CULTURAL: "Christlich / kulturell",
    COLLECTION_ISLAMIC_CULTURAL: "Islamisch / kulturell",
}

COUNTRY_PROFILE_LABELS = {
    "en": {
        "de": "Germany",
    },
    "de": {
        "de": "Deutschland",
    },
}

EVENT_COLLECTION_LABELS = {
    "en": {
        COLLECTION_CULTURAL: "General / cultural",
        COLLECTION_CHRISTIAN_CULTURAL: "Christian / cultural",
        COLLECTION_ISLAMIC_CULTURAL: "Islamic / cultural",
    },
    "de": {
        COLLECTION_CULTURAL: "Allgemein / kulturell",
        COLLECTION_CHRISTIAN_CULTURAL: "Christlich / kulturell",
        COLLECTION_ISLAMIC_CULTURAL: "Islamisch / kulturell",
    },
}

EVENT_LABELS = {
    "en": {
        EVENT_NEW_YEAR: "New Year",
        EVENT_HALLOWEEN: "Halloween",
        EVENT_ADVENT: "Advent",
        EVENT_CHRISTMAS_SEASON: "Christmas Season",
        EVENT_EASTER: "Easter",
        EVENT_RAMADAN: "Ramadan",
    },
    "de": {
        EVENT_NEW_YEAR: "Neujahr",
        EVENT_HALLOWEEN: "Halloween",
        EVENT_ADVENT: "Advent",
        EVENT_CHRISTMAS_SEASON: "Weihnachtszeit",
        EVENT_EASTER: "Ostern",
        EVENT_RAMADAN: "Ramadan",
    },
}
