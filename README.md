# Seasonal Events

[![GitHub release](https://img.shields.io/github/v/release/RF1705/Seasonal-Events?display_name=tag)](https://github.com/RF1705/Seasonal-Events/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)

Seasonal Events is a Home Assistant custom integration that exposes recurring
seasonal periods as simple entities for automations.

The integration is intended to behave like the Workday sensor pattern: keep the
date logic in one integration and keep automations small.

## Initial entities

- `binary_sensor.advent`
- `binary_sensor.christmas_season`
- `binary_sensor.new_year`
- `binary_sensor.halloween`
- `sensor.new_year_countdown`

## First region profile

The first scaffold includes a `western_christian` profile:

- Advent: first Advent Sunday through December 24
- Christmas Season: first Advent Sunday through January 6
- New Year: December 31 through January 1
- Halloween: October 31

More regional profiles can be added as data definitions.

## Automation idea

```yaml
condition:
  - condition: state
    entity_id: binary_sensor.christmas_season
    state: "on"
```

## Development status

This is an early scaffold for a new repository.

## Repository

https://github.com/RF1705/Seasonal-Events
