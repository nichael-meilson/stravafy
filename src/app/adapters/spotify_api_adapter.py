import requests
from src.utils import read_config
from src.utils.encryption import Encryption
from src.utils.spotify_auth_handler import SpotifyAuthHandler
import webbrowser
from starlette.exceptions import HTTPException

class SpotifyAPIAdapter:
    client_id: str
    client_secret: str
    session: requests.Session
    access_token: str

    def __init__(self) -> None:
        config = read_config()
        self.client_id: str = Encryption().decrypt_string(config["spotify_credentials"]["client_id"])
        self.session: requests.Session = requests.session()
        self.access_token: str = self.authorize_spotify_api()


    def authorize_spotify_api(self) -> str:
        url = f"https://accounts.spotify.com/authorize"
        redirect_uri = "http://localhost:5000"

        auth_url = f"{url}?client_id={self.client_id}&redirect_uri={redirect_uri}&response_type=code&scope=user-read-recently-played&approval_prompt=force"
        webbrowser.open(auth_url)

        handler_response = SpotifyAuthHandler()
        handler_response.handle_request()
        if handler_response.auth_code:
            token_url = "https://accounts.spotify.com/api/token"
            payload = {
                "client_id": handler_response.client_id,
                "client_secret": handler_response.client_secret,
                "code": handler_response.auth_code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri
            }
            response = requests.post(token_url, data=payload)
            access_token = response.json().get('access_token')
            return access_token
        else:
            raise HTTPException("No auth code returned")
