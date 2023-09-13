import requests
import yaml
import webbrowser
from src.utils.encryption import Encryption
from src.utils.strava_auth_handler import StravaAuthHandler
from starlette.exceptions import HTTPException
from typing import List, Dict

def read_config() -> dict:
    with open('./src/config.yaml', 'r') as stream:
        try: 
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            raise e
        

def _get_activity_ids_from_activity_list(activities: List[Dict], limit: int) -> List:
    activity_ids = []
    for activity in activities:
        activity_ids.append(activity.get("id"))
    if limit <= len(activity_ids):
        return activity_ids[0:limit]
    else:
        return activity_ids


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
            response = requests.post(token_url, data=payload, verify=False)
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
        resp = self.session.get(URL, headers=headers, params=params ,verify=False)
        return resp.json()
    
    def get_strava_activity_timeseries(self, activities: str):
        heartrates = []
        activity_ids = _get_activity_ids_from_activity_list(activities, limit=5)
        for id in activity_ids:
            url = f"https://www.strava.com/api/v3/activities/{id}/streams"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            params = {
                "key_by_type": True,
                "keys": "time,heartrate,ditance"
            }
            resp = self.session.get(url, headers=headers, params=params, verify=False)
            heartrates.append(resp.json())
        return heartrates
