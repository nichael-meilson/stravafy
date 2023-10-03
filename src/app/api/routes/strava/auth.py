from fastapi import APIRouter
from fastapi import Depends, HTTPException
from utils import read_config
from utils.encryption import Encryption
from fastapi import FastAPI, Depends, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
import requests

router = APIRouter()
config = read_config()
CLIENT_ID = Encryption().decrypt_string(config["strava_credentials"]["client_id"])
CLIENT_SECRET = Encryption().decrypt_string(config["strava_credentials"]["client_secret"])

STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
STRAVA_REDIRECT_URI = "http://localhost:8000/api/auth/strava/callback"

@router.get("/auth/strava")
def start_strava_auth(request: Request):
    # Redirect the user to the Strava OAuth authorization URL
    strava_auth_url = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={STRAVA_REDIRECT_URI}&response_type=code&scope=read,activity:read_all&approval_prompt=force"
    return RedirectResponse(url=strava_auth_url)

# Endpoint to handle the callback from Strava after authorization
@router.get("/auth/strava/callback")
async def strava_auth_callback(request: Request, code: str = Query(None)):
    # Extract the 'code' parameter from the callback URL
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code is missing")
    

    # Use the 'code' to request an access token from Strava
    token_url = "https://www.strava.com/oauth/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token from Strava")

