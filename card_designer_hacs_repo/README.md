# Card Designer

A Home Assistant integration + Lovelace card for designing and rendering Jinja templates.

## Installation (via HACS)
1. Add this repository to HACS as a custom repository.
2. Install the integration and/or frontend.
3. Restart Home Assistant.

## Manual Installation
- Copy `custom_components/card_designer` into your HA config folder.
- Copy `www/card-designer-card.js` into `<config>/www/`.
- Add the resource in Lovelace:
  ```yaml
  resources:
    - url: /local/card-designer-card.js
      type: module
  ```

## Usage
Example card:
```yaml
type: 'custom:card-designer-card'
title: Example
template: |
  <div>
    <h3>{{ title }}</h3>
    <p>Sensor: {{ states('sensor.my_sensor') }}</p>
  </div>
context:
  title: Hello
```
