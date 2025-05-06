# steam_controller.py

from fastapi.templating import Jinja2Templates
from fastapi import Request
import httpx
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta

templates = Jinja2Templates(directory="templates")
load_dotenv(override=True)

# Environment Variables
API_KEY = os.getenv('API_KEY')

# Cache em memória com validade de 1 dia
steam_cache = {}
CACHE_DURATION = timedelta(days=1)

async def getAllGamesController(request: Request, steamid: int) -> dict:
    """
    Returns all the player's games with:

    {
        "games_count": (int),
        "owned_games_info": {
            "appid": (int),
            "playtime_forever": (int)
        }
    }

    """
    async with httpx.AsyncClient() as client:
        owned_games_response = await client.get(
            f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={steamid}&format=json'
        )

        owned_games_json_data = owned_games_response.json()['response']
        owned_games_info = []

        for game in owned_games_json_data.get('games', []):
            game_info = {
                "appid": game['appid'],
                "playtime_forever": game['playtime_forever']
            }
            owned_games_info.append(game_info)

    return {"games_count": len(owned_games_info), "owned_games_info": owned_games_info}


async def getPlayerLibraryController(request: Request, steamid: int) -> dict:
    """
    Returns the player's entire library info:

    {
        "games_count": (int),
        "detailed_games_info": [{
            "appid": (int),
            "name": (str),
            "playtime_forever": (int),
            "final_price": (int),
            "final_formatted": (str),
            "is_free": (bool),
            "header_image": (str)
        }, ...]
    }
    """
    response_library = await getAllGamesController(request, steamid)
    owned_games = response_library['owned_games_info']

    async def fetch_game_details(game, client) -> dict:
        """
        Returns the game info:
        {
            "appid": (int),
            "name": (str),
            "playtime_forever": (int),
            "final_price": (int),
            "final_formatted": (str),
            "is_free": (bool),
            "header_image": (str)
        }
        """
        appid = game['appid']
        url = f'https://store.steampowered.com/api/appdetails?appids={appid}&cc=us&l=portuguese'

        try:
            response = await client.get(url)
            data = response.json()

            if data and data[str(appid)]['success']:
                game_data = data[str(appid)]['data']

                price_info = game_data.get("price_overview", {})
                final_price = price_info.get('final', 0)
                final_formatted = price_info.get('final_formatted', "R$ 0,00")

                return {
                    "appid": appid,
                    "name": game_data.get("name"),
                    "playtime_forever": game['playtime_forever'],
                    "final_price": final_price,
                    "final_formatted": final_formatted,
                    "is_free": game_data.get('is_free', False),
                    "header_image": game_data.get('header_image')
                }

        except Exception as e:
            print(f"(fetch_game_details) Erro ao buscar detalhes para o appid {appid}: {e}")
        return None 

    async with httpx.AsyncClient() as client:
        tasks = [fetch_game_details(game, client) for game in owned_games]
        results = await asyncio.gather(*tasks)

        detailed_games_info = [game for game in results if game is not None]

    return {
        'games_count': response_library['games_count'],
        "detailed_games_info": detailed_games_info
    }


async def fetch_player_data(request: Request, steamid: int) -> dict:
    """
    Returns the player's data:
    {
        "player_info": {
            "steamid": (int),
            "name": (str),
            "nickname": (str),
            "profile_url": (str),
            "avatar": (str),
            "country": (str),
            "total_games_library": (int)
        },
        "games_not_played_qtd": (int),
        "games_not_played": [
            {
                "appid": (int),
                "name": (str),
                "playtime_forever": (int),
                "final_price": (int),
                "final_formatted": (str),
                "is_free": (bool),
                "header_image": (str)
            },...],
        "total_wasted": (float),
        "total_price_library": (float)
    }
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={API_KEY}&steamids={steamid}")
    
    players = response.json().get('response', {}).get('players', [])

    if not players:
        return None

    player_info_json = players[0]
    library_response = await getPlayerLibraryController(request, steamid)
    total_games_library = library_response['games_count']

    player_info = {
        "steamid": player_info_json['steamid'],
        "name": player_info_json.get('realname'),
        "nickname": player_info_json['personaname'],
        "profile_url": player_info_json['profileurl'],
        "avatar": player_info_json['avatarfull'],
        "country": player_info_json.get('loccountrycode'),
        "total_games_library": total_games_library
    }

    games_not_played = []
    total_wasted = 0
    total_price_library = 0

    for game in library_response['detailed_games_info']:
        price = game['final_price'] / 100
        total_price_library += price

        if game['playtime_forever'] <= 0:
            games_not_played.append(game)
            total_wasted += price

    return {
        "player_info": player_info,
        "games_not_played_qtd": len(games_not_played),
        "games_not_played": games_not_played,
        "total_wasted": total_wasted,
        "total_price_library": total_price_library
    }


async def getPlayerInfo(request: Request, steamid: int):
    """
    Redirects the user to the profile.html (/steam/player) page
    """
    from datetime import timezone
    now = datetime.now(timezone.utc)
    cache_entry = steam_cache.get(steamid)

    if cache_entry and now - cache_entry['timestamp'] < CACHE_DURATION:
        data = cache_entry['data']
    else:
        data = await fetch_player_data(request, steamid)
        if data is None:
            return templates.TemplateResponse('index.html', {
                "request": request,
                "title": "Profile",
                "warning": "Player not found"
            })

        steam_cache[steamid] = {
            "data": data,
            "timestamp": now
        }

    return templates.TemplateResponse('profile.html', {
        "request": request,
        "title": "Profile",
        "player_info": data['player_info'],
        "games_not_played_qtd": data['games_not_played_qtd'],
        "games_not_played": data['games_not_played'],
        "total_wasted": data['total_wasted'],
        "total_price_library": data['total_price_library']
    })
