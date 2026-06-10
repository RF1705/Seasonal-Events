"""Config flow for Seasonal Events."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_COUNTRY_PROFILE,
    CONF_EVENT_GROUPS,
    CONF_REGION_PROFILE,
    COUNTRY_PROFILES,
    COUNTRY_PROFILE_LABELS,
    DEFAULT_COUNTRY_PROFILE,
    DEFAULT_EVENT_GROUPS,
    DOMAIN,
    EVENT_GROUP_LABELS,
)


def _localized_labels(
    labels: dict[str, dict[str, str]],
    language: str | None,
    fallback: dict[str, str],
) -> dict[str, str]:
    """Return localized labels."""
    if language:
        language = language.split("-")[0]
    return labels.get(language or "en", labels["en"]) | {
        key: labels.get(language or "en", labels["en"]).get(key, value)
        for key, value in fallback.items()
    }


def _select_options(items: dict[str, str]) -> list[selector.SelectOptionDict]:
    """Return selector options."""
    return [
        selector.SelectOptionDict(value=value, label=label)
        for value, label in items.items()
    ]


def _event_group_options(language: str | None) -> list[selector.SelectOptionDict]:
    """Return event group selector options."""
    labels = _localized_labels(EVENT_GROUP_LABELS, language, {})
    return [
        selector.SelectOptionDict(value=value, label=label)
        for value, label in labels.items()
    ]


def _schema(
    defaults: dict[str, Any] | None = None,
    language: str | None = None,
) -> vol.Schema:
    """Return the config schema."""
    defaults = defaults or {}
    country_profile = defaults.get(
        CONF_COUNTRY_PROFILE,
        defaults.get(CONF_REGION_PROFILE, DEFAULT_COUNTRY_PROFILE),
    )
    country_labels = _localized_labels(
        COUNTRY_PROFILE_LABELS,
        language,
        COUNTRY_PROFILES,
    )
    return vol.Schema(
        {
            vol.Required(
                CONF_COUNTRY_PROFILE,
                default=country_profile,
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_select_options(country_labels),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_EVENT_GROUPS,
                default=defaults.get(CONF_EVENT_GROUPS, DEFAULT_EVENT_GROUPS),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_event_group_options(language),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
        }
    )


class SeasonalEventsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Seasonal Events."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            user_input[CONF_REGION_PROFILE] = user_input[CONF_COUNTRY_PROFILE]
            country_labels = _localized_labels(
                COUNTRY_PROFILE_LABELS,
                self.hass.config.language,
                COUNTRY_PROFILES,
            )
            return self.async_create_entry(
                title=country_labels[user_input[CONF_COUNTRY_PROFILE]],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_schema(language=self.hass.config.language),
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return SeasonalEventsOptionsFlow(config_entry)


class SeasonalEventsOptionsFlow(config_entries.OptionsFlow):
    """Handle Seasonal Events options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Manage integration options."""
        if user_input is not None:
            user_input[CONF_REGION_PROFILE] = user_input[CONF_COUNTRY_PROFILE]
            return self.async_create_entry(title="", data=user_input)

        current = {**self._config_entry.data, **self._config_entry.options}
        return self.async_show_form(
            step_id="init",
            data_schema=_schema(current, self.hass.config.language),
        )
