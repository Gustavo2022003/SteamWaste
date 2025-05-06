from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

import routers.index_router
import routers.steam_router

# Config
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/public", StaticFiles(directory="./templates/public"), name="public")

# Routers
import routers
app.include_router(routers.index_router.router)
app.include_router(routers.steam_router.router, prefix='/steam')