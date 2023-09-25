from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import requests
from urllib.parse import urlencode
from utils import read_config
from utils.encryption import Encryption

router = APIRouter()

config = read_config()

# Endpoint to initiate Strava OAuth flow
@router.get("/auth")
def start_strava_auth(request: Request):
    strava_auth_url = (
        "https://www.strava.com/oauth/authorize?"
        + urlencode(
            {
                "client_id": Encryption().decrypt_string(config["strava_credentials"]["client_id"]),
                "redirect_uri": config["strava_credentials"]["redirect_uri"],
                "response_type": "code",
                "scope": "read,activity:read_all",
                "approval_prompt": "force",
            }
        )
    )
    return RedirectResponse(url=strava_auth_url)

# Callback route to handle Strava authorization callback
@router.get("/auth/callback")
def strava_auth_callback(code: str, state: str = None):
    global authorization_code
    authorization_code = code
    return {"message": "Strava authorization code received. You can close this tab now."}

# Endpoint to exchange authorization code for access token
@router.get("/get_access_token")
def get_access_token():
    global authorization_code
    if authorization_code is None:
        raise HTTPException(status_code=403, detail="No authorization code received")

    token_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": Encryption().decrypt_string(config["strava_credentials"]["client_id"]),
        "client_secret": Encryption().decrypt_string(config["strava_credentials"]["client_secret"]),
        "code": authorization_code,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to obtain access token")
