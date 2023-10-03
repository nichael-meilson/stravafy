from utils import read_config, convert_string_date_to_epoch
from utils.encryption import Encryption
from fastapi import APIRouter, HTTPException
from fastapi import HTTPException, Request, Query
from fastapi.responses import RedirectResponse
import requests
import os

router = APIRouter()
config = read_config()

STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_REDIRECT_URI = "http://localhost:8000/api/auth/strava/callback"

@router.get("/auth/strava", tags=["auth"])
def start_strava_auth(request: Request):
    client_id = Encryption().decrypt_string(config["strava_credentials"]["client_id"])
    strava_auth_url = f"https://www.strava.com/oauth/authorize?client_id={client_id}&redirect_uri={STRAVA_REDIRECT_URI}&response_type=code&scope=read,activity:read_all&approval_prompt=force"
    return RedirectResponse(url=strava_auth_url)

# Endpoint to handle the callback from Strava after authorization
@router.get("/auth/strava/callback", tags=["auth"])
async def strava_auth_callback(request: Request, code: str = Query(None)):

    if not code:
        raise HTTPException(status_code=400, detail="Authorization code is missing")

    # Use the 'code' to request an access token from Strava
    token_url = "https://www.strava.com/oauth/token"
    data = {
        "client_id": Encryption().decrypt_string(config["strava_credentials"]["client_id"]),
        "client_secret": Encryption().decrypt_string(config["strava_credentials"]["client_secret"]),
        "code": code,
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        os.environ["STRAVA_ACCESS_TOKEN"] = response.json().get("access_token")
        return "Strava access token received - this tab can be closed"
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token from Strava")

