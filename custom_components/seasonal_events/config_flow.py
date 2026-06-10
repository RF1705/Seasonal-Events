"""Config flow for Seasonal Events."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    CONF_ENABLED_EVENTS,
    CONF_REGION_PROFILE,
    DEFAULT_EVENTS,
    DEFAULT_REGION_PROFILE,
    DOMAIN,
    REGION_PROFILES,
)


def _schema(defaults: dict[str, Any] | None = None) -> vol.Schema:
    """Return the config schema."""
    defaults = defaults or {}
    return vol.Schema(
        {
            vol.Required(
                CONF_REGION_PROFILE,
                default=defaults.get(CONF_REGION_PROFILE, DEFAULT_REGION_PROFILE),
            ): vol.In(REGION_PROFILES),
            vol.Required(
                CONF_ENABLED_EVENTS,
                default=defaults.get(CONF_ENABLED_EVENTS, DEFAULT_EVENTS),
            ): cv_multi_select(DEFAULT_EVENTS),
        }
    )


def cv_multi_select(options: list[str]):
    """Validate a multi-select list."""

    def validator(value: Any) -> list[str]:
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list):
            raise vol.Invalid("expected list")
        unknown = set(value) - set(options)
        if unknown:
            raise vol.Invalid(f"unknown options: {unknown}")
        return value

    return validator


class SeasonalEventsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Seasonal Events."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(
                title="Seasonal Events",
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
            return self.async_create_entry(title="", data=user_input)

        current = {**self._config_entry.data, **self._config_entry.options}
        return self.async_show_form(
            step_id="init",
            data_schema=_schema(current),
        )
