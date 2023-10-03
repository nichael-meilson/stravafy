from utils import read_config
from utils.encryption import Encryption
from fastapi import APIRouter, HTTPException
from fastapi import HTTPException, Request, Query
from fastapi.responses import RedirectResponse
import requests
import os

router = APIRouter()
config = read_config()

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
REDIRECT_URI = "http://localhost:8000/api/auth/spotify/callback"

@router.get("/auth/spotify", tags=["auth"])
def start_spotify_auth(request: Request):
    client_id = Encryption().decrypt_string(config["spotify_credentials"]["client_id"])
    auth_url = f"{AUTH_URL}?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code&scope=user-read-recently-played&approval_prompt=force"
    return RedirectResponse(url=auth_url)

@router.get("/auth/spotify/callback", tags=["auth"])
async def spotify_auth_callback(request: Request, code: str = Query(None)):
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code is missing")

    data = {
        "client_id": Encryption().decrypt_string(config["spotify_credentials"]["client_id"]),
        "client_secret": Encryption().decrypt_string(config["spotify_credentials"]["client_secret"]),
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, data=data)

    if response.status_code == 200:
        os.environ["SPOTIFY_ACCESS_TOKEN"] = response.json().get("access_token")
        return "Spotify access token received - this tab can be closed"
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token from Spotify")

