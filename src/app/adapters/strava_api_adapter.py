import requests
import yaml
import webbrowser
from src.utils.encryption import Encryption

def read_config() -> dict:
    with open('./src/config.yaml', 'r') as stream:
        try: 
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            raise e

class StravaAPIAdapter:
    def __init__(self) -> None:
        config = read_config()
        self.client_id: str = Encryption().decrypt_string(config["strava_credentials"]["client_id"])
        self.session: requests.Session = requests.session()

    def authorize_strava_api(self):
        url = f"https://www.strava.com/oauth/authorize"
        redirect_uri = "https://localhost/exchange_token"

        auth_url = f"{url}?client_id={self.client_id}&redirect_uri={redirect_uri}&response_type=code&scope=read&approval_prompt=force"
        webbrowser.open(auth_url)
        pass

    def get_strava_athlete_activities(self):
        session = self.session()
        URL = "https://www.strava.com/api/v3/athlete/activities"
        headers = {"Authorization": "Bearer "}
        params = {
            "before": 1692061200,
            "after": 1672534800
        }
        resp = session.get(URL, headers=headers, params=params)
        return resp.json()
    
    def get_strava_activity_timeseries():
        pass