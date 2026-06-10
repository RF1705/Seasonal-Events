"""Config flow for Seasonal Events."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    CONF_COUNTRY_PROFILE,
    CONF_ENABLED_EVENTS,
    CONF_EVENT_COLLECTIONS,
    CONF_NAME,
    CONF_REGION_PROFILE,
    COUNTRY_PROFILES,
    DEFAULT_COUNTRY_PROFILE,
    DEFAULT_EVENT_COLLECTIONS,
    DEFAULT_EVENTS,
    DEFAULT_NAME,
    DEFAULT_REGION_PROFILE,
    DOMAIN,
    EVENT_COLLECTIONS,
    EVENTS,
    REGION_PROFILES,
)


def _select_options(items: dict[str, str]) -> list[selector.SelectOptionDict]:
    """Return selector options."""
    return [
        selector.SelectOptionDict(value=value, label=label)
        for value, label in items.items()
    ]


def _event_options() -> list[selector.SelectOptionDict]:
    """Return event selector options."""
    return [
        selector.SelectOptionDict(value=value, label=str(data["name"]))
        for value, data in EVENTS.items()
    ]


def _schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    """Return the config schema."""
    defaults = defaults or {}
    country_profile = defaults.get(
        CONF_COUNTRY_PROFILE,
        defaults.get(CONF_REGION_PROFILE, DEFAULT_COUNTRY_PROFILE),
    )
    return vol.Schema(
        {
            vol.Required(
                CONF_NAME,
                default=defaults.get(CONF_NAME, DEFAULT_NAME),
            ): selector.TextSelector(),
            vol.Required(
                CONF_COUNTRY_PROFILE,
                default=country_profile,
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_select_options(COUNTRY_PROFILES),
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            ),
            vol.Required(
                CONF_EVENT_COLLECTIONS,
                default=defaults.get(
                    CONF_EVENT_COLLECTIONS,
                    DEFAULT_EVENT_COLLECTIONS,
                ),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_select_options(EVENT_COLLECTIONS),
                    multiple=True,
                    mode=selector.SelectSelectorMode.LIST,
                )
            ),
            vol.Required(
                CONF_ENABLED_EVENTS,
                default=defaults.get(CONF_ENABLED_EVENTS, DEFAULT_EVENTS),
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=_event_options(),
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
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_schema(),
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
            data_schema=_schema(current),
        )
