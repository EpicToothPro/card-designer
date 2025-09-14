"""Card Designer custom integration for Home Assistant."""
from http import HTTPStatus
from homeassistant.core import HomeAssistant
from homeassistant.helpers import template as template_helper
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.http import HomeAssistantView

DOMAIN = "card_designer"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    hass.http.register_view(RenderView(hass))
    return True

class RenderView(HomeAssistantView):
    url = "/api/card_designer/render"
    name = "api:card_designer:render"

    def __init__(self, hass: HomeAssistant):
        self.hass = hass

    async def post(self, request):
        try:
            data = await request.json()
        except Exception:
            return self.json({"error": "invalid_json"}, status_code=HTTPStatus.BAD_REQUEST)

        template_str = data.get("template", "")
        context = data.get("context", {}) or {}
        try:
            tpl = template_helper.Template(template_str, self.hass)
            result = tpl.async_render(context)
        except Exception as e:
            return self.json({"error": "render_failed", "message": str(e)}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        return self.json({"result": result})
