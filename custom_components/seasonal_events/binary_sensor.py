"""Binary sensors for Seasonal Events."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .calendar_engine import active_or_next_window
from .const import (
    CONF_COUNTRY_PROFILE,
    CONF_ENABLED_EVENTS,
    CONF_NAME,
    CONF_REGION_PROFILE,
    DEFAULT_EVENTS,
    DEFAULT_NAME,
    DEFAULT_REGION_PROFILE,
    DOMAIN,
    EVENTS,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Seasonal Events binary sensors."""
    config = {**entry.data, **entry.options}
    enabled_events = config.get(CONF_ENABLED_EVENTS, DEFAULT_EVENTS)
    enabled_events = [
        event_key
        for event_key in enabled_events
        if event_key in EVENTS
    ]
    region_profile = config.get(
        CONF_COUNTRY_PROFILE,
        config.get(CONF_REGION_PROFILE, DEFAULT_REGION_PROFILE),
    )

    async_add_entities(
        SeasonalEventBinarySensor(
            hass,
            entry.entry_id,
            config.get(CONF_NAME, entry.title or DEFAULT_NAME),
            event_key,
            region_profile,
        )
        for event_key in enabled_events
    )


class SeasonalEventBinarySensor(BinarySensorEntity):
    """Binary sensor for a seasonal event window."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry_id: str,
        device_name: str,
        event_key: str,
        region_profile: str,
    ) -> None:
        """Initialize the entity."""
        self.hass = hass
        self._entry_id = entry_id
        self._device_name = device_name
        self._event_key = event_key
        self._region_profile = region_profile
        self._window = None
        self._attr_unique_id = f"{entry_id}_{event_key}"
        self.entity_description = BinarySensorEntityDescription(
            key=event_key,
            translation_key=str(EVENTS[event_key]["translation_key"]),
        )
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            manufacturer="Seasonal Events",
            name=self._device_name,
            model="Seasonal event calendar",
        )

    @property
    def icon(self) -> str | None:
        """Return the icon."""
        return self._window.icon if self._window else None

    @property
    def is_on(self) -> bool:
        """Return true if the event is active."""
        if self._window is None:
            self._update_window()
        return self._window.contains(dt_util.now().date()) if self._window else False

    @property
    def extra_state_attributes(self) -> dict[str, str | int] | None:
        """Return extra attributes."""
        if self._window is None:
            self._update_window()
        if self._window is None:
            return None

        today = dt_util.now().date()
        return {
            "event_key": self._event_key,
            "region_profile": self._region_profile,
            "country_profile": self._region_profile,
            "start_date": self._window.start.isoformat(),
            "end_date": self._window.end.isoformat(),
            "days_until_start": self._window.days_until_start(today),
            "days_until_end": self._window.days_until_end(today),
        }

    async def async_added_to_hass(self) -> None:
        """Register update callbacks."""
        self._update_window()
        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                self._handle_time_update,
                timedelta(minutes=1),
            )
        )

    @callback
    def _handle_time_update(self, _) -> None:
        """Handle periodic updates."""
        self._update_window()
        self.async_write_ha_state()

    def _update_window(self) -> None:
        """Update the cached event window."""
        self._window = active_or_next_window(
            self._event_key,
            dt_util.now().date(),
            self._region_profile,
        )
