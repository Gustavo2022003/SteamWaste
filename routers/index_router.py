# index_router.py

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from controllers.index_controller import getIndex, troubleshootingRender

router = APIRouter()

@router.get("/")
async def index(request: Request):
    return RedirectResponse(url='/home')

@router.get("/troubleshooting")
async def troubleshooting(request: Request):
    return await troubleshootingRender(request)

@router.get("/home")
async def home(request: Request):
    return await getIndex(request)
