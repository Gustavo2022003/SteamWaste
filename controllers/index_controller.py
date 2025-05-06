# index_controller.py

from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

async def troubleshootingRender(request: Request):
    return templates.TemplateResponse('troubleshooting.html', {
            "request": request,
            "title": "Troubleshooting"
        })

async def getIndex(request: Request):
    return templates.TemplateResponse('index.html', {
            "request": request,
            "title": "Home"
        })
