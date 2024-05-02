__version__ = "0.1.0"
__author__ = "Zac Foteff"
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="api/templates")


class DefaultController:
    async def render_homepage(request: Request) -> HTMLResponse:
        return templates.TemplateResponse(
            "home.html", request=request, context={"request": ""}
        )
