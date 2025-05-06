# steam_router.py

from fastapi import APIRouter, Request, Form
from controllers.steam_controller import getPlayerInfo, getPlayerLibraryController

router = APIRouter()

# Returns the player's entire library with info
@router.get("/getPlayerLibrary")
async def getPlayerLibraryRouter(request: Request, steamid: int):
    return await getPlayerLibraryController(request, steamid)

# Redirects the user to the profile.html with all player's info needed
@router.post('/player')
async def getPlayerInfoRoute(request: Request, steamid: str = Form(...)):
    return await getPlayerInfo(request, steamid)

# Get all appids from a user's steamid
@router.get('/getAllAppids')
async def getAllAppids(request: Request, steamid:int):
    from controllers.steam_controller import getAllGamesController
    return await getAllGamesController(request, steamid)