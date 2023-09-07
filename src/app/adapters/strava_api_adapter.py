import requests
import yaml
import webbrowser
from src.utils.encryption import Encryption
from src.utils.strava_auth_handler import StravaAuthHandler
from starlette.exceptions import HTTPException

def read_config() -> dict:
    with open('./src/config.yaml', 'r') as stream:
        try: 
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            raise e

class StravaAPIAdapter:
    client_id: str
    session: requests.Session
    access_token: str

    def __init__(self) -> None:
        config = read_config()
        self.client_id: str = Encryption().decrypt_string(config["strava_credentials"]["client_id"])
        self.session: requests.Session = requests.session()
        self.access_token: str = self.authorize_strava_api()

    def authorize_strava_api(self) -> str:
        url = f"https://www.strava.com/oauth/authorize"
        redirect_uri = "http://localhost:5000"

        auth_url = f"{url}?client_id={self.client_id}&redirect_uri={redirect_uri}&response_type=code&scope=read&scope=activity:read_all&approval_prompt=force"
        webbrowser.open(auth_url)

        handler_response = StravaAuthHandler()
        handler_response.handle_request()
        if handler_response.auth_code:
            token_url = "https://www.strava.com/oauth/token"
            payload = {
                "client_id": handler_response.client_id,
                "client_secret": handler_response.client_secret,
                "code": handler_response.auth_code,
                "grant_type": "authorization_code"
            }
            response = requests.post(token_url, data=payload)
            access_token = response.json().get('access_token')
            return access_token
        else:
            raise HTTPException("No auth code returned")
        
    def get_strava_athlete(self):
        URL = "https://www.strava.com/api/v3/athlete"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        resp = self.session.get(URL, headers=headers)
        return resp.json()

    def get_strava_athlete_activities(self):
        URL = "https://www.strava.com/api/v3/athlete/activities"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "before": 1692061200,
            "after": 1672534800
        }
        resp = self.session.get(URL, headers=headers, params=params)
        return resp.json()
    
    def get_strava_activity_timeseries():
        pass