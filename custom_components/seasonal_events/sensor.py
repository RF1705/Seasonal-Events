"""Sensors for Seasonal Events."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .calendar_engine import new_year_countdown


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Seasonal Events sensors."""
    async_add_entities([NewYearCountdownSensor(hass, entry.entry_id)])


class NewYearCountdownSensor(SensorEntity):
    """Countdown to the next New Year."""

    _attr_has_entity_name = True
    _attr_name = "New Year Countdown"
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_icon = "mdi:timer-sand"

    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._attr_unique_id = f"{entry_id}_new_year_countdown"
        self._countdown: dict[str, int | str] = {}

    @property
    def native_value(self) -> int | None:
        """Return seconds until New Year."""
        if not self._countdown:
            self._update_countdown()
        return self._countdown.get("total_seconds")

    @property
    def extra_state_attributes(self) -> dict[str, int | str]:
        """Return countdown details."""
        if not self._countdown:
            self._update_countdown()
        return self._countdown

    async def async_added_to_hass(self) -> None:
        """Register update callbacks."""
        self._update_countdown()
        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                self._handle_time_update,
                timedelta(seconds=1),
            )
        )

    @callback
    def _handle_time_update(self, _) -> None:
        """Handle periodic updates."""
        self._update_countdown()
        self.async_write_ha_state()

    def _update_countdown(self) -> None:
        """Update countdown state."""
        self._countdown = new_year_countdown(dt_util.now())
