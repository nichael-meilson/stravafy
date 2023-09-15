import requests
import webbrowser
from datetime import datetime
from src.utils import read_config
from src.utils.encryption import Encryption
from src.utils.strava_auth_handler import StravaAuthHandler
from src.models.activities import Activity
from starlette.exceptions import HTTPException
from typing import List, Dict

def _convert_string_date_to_epoch(date: str) -> int:
    date_object = datetime.strptime(date, "%Y-%m-%d")
    epoch_time = (date_object - datetime(1970, 1, 1)).total_seconds()
    return epoch_time 


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

    def get_strava_activities(self, start: str, end: str) -> str:
        start_epoch = _convert_string_date_to_epoch(start)
        end_epoch = _convert_string_date_to_epoch(end)

        URL = "https://www.strava.com/api/v3/athlete/activities"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "before": end_epoch,
            "after": start_epoch
        }
        resp = self.session.get(URL, headers=headers, params=params ,verify=False)
        return resp.json()
    
    def model_strava_activities(self, activities: List) -> List[Activity]:
        modelled_activities_list = []
        for activity in activities:
            modelled_activity = Activity(
                id=activity.get('id'),
                athlete_id=activity.get('athlete').get('id'),
                activity_type=activity.get('type'),
                timezone=activity.get('timezone'),
                start_date=activity.get('start_date'),
                suffer_score=activity.get('suffer_score')                
            )
            modelled_activities_list.append(modelled_activity)
        return modelled_activities_list
    
    def get_strava_activity_streams(self, activities: List[Activity]) -> List[Activity]:
        """
        Adds streams to activities
        """
        activities_with_streams = []
        for activity in activities:
            url = f"https://www.strava.com/api/v3/activities/{activity.id}/streams"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            params = {
                "key_by_type": True,
                "keys": "time,heartrate,ditance"
            }
            resp = self.session.get(url, headers=headers, params=params, verify=False)
            activity.set_streams(resp.json())
            activities_with_streams.append(activity)
        return activities_with_streams


