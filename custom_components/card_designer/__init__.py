"""Card Designer custom integration for Home Assistant.

Provides:
- /api/card_designer/render (POST) -> render Jinja template server-side using hass template engine.
- static files served via the panel (see panel html in www/panel)
Note: This is a minimal example. For production, sanitize input and add authentication/permissions.
"""
from http import HTTPStatus
import asyncio
import json
import os
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import template as template_helper
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.http import HomeAssistantView

DOMAIN = "card_designer"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Card Designer integration."""

    # Register a simple HTTP view to render templates server-side.
    async def render_template(request):
        hass_view = RenderView(hass)
        return await hass_view.post(request)

    hass.http.register_view(RenderView(hass))

    # Serve the panel static files under /card_designer/panel/ - uses hass.http to serve from this package
    root = os.path.dirname(__file__)
    static_path = os.path.join(root, "www", "panel")
    if os.path.isdir(static_path):
        hass.http.register_static_path("/card_designer/panel", static_path, False)

    return True


class RenderView(HomeAssistantView):
    url = "/api/card_designer/render"
    name = "api:card_designer:render"

    def __init__(self, hass: HomeAssistant):
        self.hass = hass

    async def post(self, request):
        """Render a jinja template sent in JSON body {template: ..., context: {...}}"""
        try:
            data = await request.json()
        except Exception:
            return self.json({"error": "invalid_json"}, status_code=HTTPStatus.BAD_REQUEST)

        template_str = data.get("template", "")
        context = data.get("context", {}) or {}

        # Use Home Assistant template engine to render safely
        try:
            tpl = template_helper.Template(template_str, self.hass)
            result = tpl.async_render(context)
        except Exception as e:
            return self.json({"error": "render_failed", "message": str(e)}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        return self.json({"result": result})

