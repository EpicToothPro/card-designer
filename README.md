# Card Designer (HACS-ready package)

This package contains a minimal Home Assistant custom integration and a Lovelace custom card plus a local web UI to design cards using Jinja, YAML, HTML and small Python-based rendering on the Home Assistant server.

**What's inside**
- `custom_components/card_designer/` - Home Assistant integration that provides a simple `/api/card_designer/render` endpoint to render Jinja templates using Home Assistant's template engine and serves a local design panel.
- `card_designer/www/card-designer-card.js` - a Lovelace custom card that can render HTML returned from the backend and can be used in Lovelace dashboards.
- `card_designer/www/panel/index.html` - a small local web UI you can open at `https://<your_ha_host>/card_designer/panel/` to design cards.

**Security note:** This is a demo. Do not expose your Home Assistant instance to untrusted networks with this enabled. The integration renders templates server-side; avoid rendering untrusted templates. Consider adding authentication checks if needed.

## Install (manual / HACS zip)
1. In Home Assistant, go to **Settings > Add-ons & Backups > File Editor** (or use Samba / SSH) and upload the extracted files so that `custom_components/card_designer` appears in your HA config directory.
2. Place `card-designer-card.js` under `<config>/www/community/card_designer/` (or keep it inside `custom_components/card_designer/www/` and point to it)
3. Restart Home Assistant.
4. In Lovelace raw config, add the resource (if using YAML mode or resource management):
   ```yaml
   resources:
     - url: /local/community/card_designer/card-designer-card.js
       type: module
   ```
   or if served from the integration's static path:
   ```yaml
   resources:
     - url: /card_designer/panel/card-designer-card.js
       type: module
   ```
5. Add the card in Lovelace as a manual card:
   ```yaml
   type: 'custom:card-designer-card'
   title: Example
   template: |
     <div>
       <h3>{{ title }}</h3>
       <p>Sensor value: {{ states('sensor.my_sensor') }}</p>
     </div>
   context:
     title: Hello from Jinja
   ```

## Install to HACS
HACS expects a GitHub repository. Two common approaches:
1. Create a GitHub repo, push the package (root should contain `custom_components/` and `card_designer/`), then add the repo to HACS:
   - In HACS -> Settings -> Custom repositories -> Add -> enter your repo URL and select category (Integration and/or Frontend)
   - Install from HACS
2. HACS also supports installing from a ZIP file if you host the ZIP on a URL (e.g., GitHub Releases). Upload the provided ZIP to a GitHub release and add the release URL to HACS as a custom repo, or install via HACS -> Integrations -> three dots -> "Install from URL" (depending on HACS version).

## Usage
- Open `https://<your_ha_host>/card_designer/panel/` to use the local web UI to craft templates and preview results.
- Use the Lovelace card to place templates in dashboards.

## License
MIT
