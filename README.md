# Seasonal Events

[![GitHub release](https://img.shields.io/github/v/release/RF1705/Seasonal-Events?display_name=tag)](https://github.com/RF1705/Seasonal-Events/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://hacs.xyz/)

Seasonal Events is a Home Assistant custom integration that exposes recurring
seasonal periods as simple entities for automations.

The integration is intended to behave like the Workday sensor pattern: keep the
date logic in one integration and keep automations small.

## Configuration

Create a calendar profile, for example `Deutschland`, choose a country profile,
and select the individual events you want to expose as sensors.

## Initial entities

- `binary_sensor.advent`
- `binary_sensor.christmas_season`
- `binary_sensor.new_year`
- `binary_sensor.halloween`
- `binary_sensor.easter`
- `binary_sensor.ramadan`
- `binary_sensor.eid_al_fitr`
- `binary_sensor.eid_al_adha`
- `binary_sensor.ashura`
- `binary_sensor.lailat_al_qadr`
- `binary_sensor.rosh_hashanah`
- `binary_sensor.yom_kippur`
- `binary_sensor.sukkot`
- `binary_sensor.hanukkah`
- `binary_sensor.passover`
- `binary_sensor.shavuot`
- `binary_sensor.purim`
- `sensor.new_year_countdown`

## Country profiles

The first scaffold includes visible differences between these profiles:

- Germany (`de`)
- United States (`us`)
- United Kingdom (`gb`)
- Israel (`il`)
- Saudi Arabia (`sa`)

- Advent: first Advent Sunday through December 24
- Christmas Season: first Advent Sunday through January 6
- New Year: December 31 through January 1
- Halloween: October 31
- Easter: Good Friday through Easter Monday
- Jewish events: calculated Hebrew calendar
- Islamic events: calculated tabular Islamic calendar

Islamic dates can differ by country or moon-sighting practice. The current
implementation is deterministic and suitable for automations, but regional
Islamic calendar modes can be added later.

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
