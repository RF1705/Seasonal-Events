"""Constants for Seasonal Events."""

from __future__ import annotations

DOMAIN = "seasonal_events"

CONF_NAME = "name"
CONF_COUNTRY_PROFILE = "country_profile"
CONF_REGION_PROFILE = "region_profile"
CONF_ENABLED_EVENTS = "enabled_events"

DEFAULT_NAME = "Deutschland"
DEFAULT_COUNTRY_PROFILE = "de"
DEFAULT_REGION_PROFILE = DEFAULT_COUNTRY_PROFILE

EVENT_ADVENT = "advent"
EVENT_CHRISTMAS_SEASON = "christmas_season"
EVENT_NEW_YEAR = "new_year"
EVENT_HALLOWEEN = "halloween"
EVENT_EASTER = "easter"
EVENT_RAMADAN = "ramadan"
EVENT_EID_AL_FITR = "eid_al_fitr"
EVENT_EID_AL_ADHA = "eid_al_adha"
EVENT_ASHURA = "ashura"
EVENT_LAILAT_AL_QADR = "lailat_al_qadr"
EVENT_ROSH_HASHANAH = "rosh_hashanah"
EVENT_YOM_KIPPUR = "yom_kippur"
EVENT_SUKKOT = "sukkot"
EVENT_HANUKKAH = "hanukkah"
EVENT_PASSOVER = "passover"
EVENT_SHAVUOT = "shavuot"
EVENT_PURIM = "purim"
EVENT_THANKSGIVING = "thanksgiving"
EVENT_GUY_FAWKES_NIGHT = "guy_fawkes_night"
EVENT_GERMAN_UNITY_DAY = "german_unity_day"
EVENT_YOM_HAATZMAUT = "yom_haatzmaut"
EVENT_SAUDI_NATIONAL_DAY = "saudi_national_day"

DEFAULT_EVENTS = [
    EVENT_NEW_YEAR,
    EVENT_HALLOWEEN,
    EVENT_CHRISTMAS_SEASON,
    EVENT_EASTER,
    EVENT_RAMADAN,
    EVENT_EID_AL_FITR,
    EVENT_EID_AL_ADHA,
    EVENT_ROSH_HASHANAH,
    EVENT_YOM_KIPPUR,
    EVENT_PASSOVER,
]

COUNTRY_PROFILES = {
    "de": "Deutschland",
    "us": "United States",
    "gb": "United Kingdom",
    "il": "Israel",
    "sa": "Saudi Arabia",
}

REGION_PROFILES = COUNTRY_PROFILES

EVENTS = {
    EVENT_NEW_YEAR: {
        "translation_key": "new_year",
    },
    EVENT_HALLOWEEN: {
        "translation_key": "halloween",
    },
    EVENT_ADVENT: {
        "translation_key": "advent",
    },
    EVENT_CHRISTMAS_SEASON: {
        "translation_key": "christmas_season",
    },
    EVENT_EASTER: {
        "translation_key": "easter",
    },
    EVENT_RAMADAN: {
        "translation_key": "ramadan",
    },
    EVENT_EID_AL_FITR: {
        "translation_key": "eid_al_fitr",
    },
    EVENT_EID_AL_ADHA: {
        "translation_key": "eid_al_adha",
    },
    EVENT_ASHURA: {
        "translation_key": "ashura",
    },
    EVENT_LAILAT_AL_QADR: {
        "translation_key": "lailat_al_qadr",
    },
    EVENT_ROSH_HASHANAH: {
        "translation_key": "rosh_hashanah",
    },
    EVENT_YOM_KIPPUR: {
        "translation_key": "yom_kippur",
    },
    EVENT_SUKKOT: {
        "translation_key": "sukkot",
    },
    EVENT_HANUKKAH: {
        "translation_key": "hanukkah",
    },
    EVENT_PASSOVER: {
        "translation_key": "passover",
    },
    EVENT_SHAVUOT: {
        "translation_key": "shavuot",
    },
    EVENT_PURIM: {
        "translation_key": "purim",
    },
    EVENT_THANKSGIVING: {
        "translation_key": "thanksgiving",
    },
    EVENT_GUY_FAWKES_NIGHT: {
        "translation_key": "guy_fawkes_night",
    },
    EVENT_GERMAN_UNITY_DAY: {
        "translation_key": "german_unity_day",
    },
    EVENT_YOM_HAATZMAUT: {
        "translation_key": "yom_haatzmaut",
    },
    EVENT_SAUDI_NATIONAL_DAY: {
        "translation_key": "saudi_national_day",
    },
}

COUNTRY_PROFILE_LABELS = {
    "en": {
        "de": "Germany",
        "us": "United States",
        "gb": "United Kingdom",
        "il": "Israel",
        "sa": "Saudi Arabia",
    },
    "de": {
        "de": "Deutschland",
        "us": "USA",
        "gb": "Vereinigtes Koenigreich",
        "il": "Israel",
        "sa": "Saudi-Arabien",
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
        EVENT_EID_AL_FITR: "Eid al-Fitr",
        EVENT_EID_AL_ADHA: "Eid al-Adha",
        EVENT_ASHURA: "Ashura",
        EVENT_LAILAT_AL_QADR: "Lailat al-Qadr",
        EVENT_ROSH_HASHANAH: "Rosh Hashanah",
        EVENT_YOM_KIPPUR: "Yom Kippur",
        EVENT_SUKKOT: "Sukkot",
        EVENT_HANUKKAH: "Hanukkah",
        EVENT_PASSOVER: "Passover",
        EVENT_SHAVUOT: "Shavuot",
        EVENT_PURIM: "Purim",
        EVENT_THANKSGIVING: "Thanksgiving",
        EVENT_GUY_FAWKES_NIGHT: "Guy Fawkes Night",
        EVENT_GERMAN_UNITY_DAY: "German Unity Day",
        EVENT_YOM_HAATZMAUT: "Yom Ha'atzmaut",
        EVENT_SAUDI_NATIONAL_DAY: "Saudi National Day",
    },
    "de": {
        EVENT_NEW_YEAR: "Neujahr",
        EVENT_HALLOWEEN: "Halloween",
        EVENT_ADVENT: "Advent",
        EVENT_CHRISTMAS_SEASON: "Weihnachtszeit",
        EVENT_EASTER: "Ostern",
        EVENT_RAMADAN: "Ramadan",
        EVENT_EID_AL_FITR: "Eid al-Fitr",
        EVENT_EID_AL_ADHA: "Eid al-Adha",
        EVENT_ASHURA: "Aschura",
        EVENT_LAILAT_AL_QADR: "Lailat al-Qadr",
        EVENT_ROSH_HASHANAH: "Rosch ha-Schana",
        EVENT_YOM_KIPPUR: "Jom Kippur",
        EVENT_SUKKOT: "Sukkot",
        EVENT_HANUKKAH: "Chanukka",
        EVENT_PASSOVER: "Pessach",
        EVENT_SHAVUOT: "Schawuot",
        EVENT_PURIM: "Purim",
        EVENT_THANKSGIVING: "Thanksgiving",
        EVENT_GUY_FAWKES_NIGHT: "Guy Fawkes Night",
        EVENT_GERMAN_UNITY_DAY: "Tag der Deutschen Einheit",
        EVENT_YOM_HAATZMAUT: "Jom haAtzma'ut",
        EVENT_SAUDI_NATIONAL_DAY: "Saudi National Day",
    },
}
