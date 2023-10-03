import requests
import os
from utils import read_config, convert_string_date_to_epoch
from utils.encryption import Encryption
from utils.strava_auth_handler import StravaAuthHandler
from models.activities import Activity
from starlette.exceptions import HTTPException
from typing import List, Dict


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
        """
        Only works after the user has called the /auth/strava endpoint
        Only works if STRAVA_ACCESS_TOKEN is in an env var
        """
        access_token = os.environ.get("STRAVA_ACCESS_TOKEN")
        if access_token:
            return access_token
        else:
            raise "No auth token returned - did the user authorize Strava?"

    def get_strava_activities(self, start: str, end: str) -> str:
        start_epoch = convert_string_date_to_epoch(start)
        end_epoch = convert_string_date_to_epoch(end)

        URL = "https://www.strava.com/api/v3/athlete/activities"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "before": end_epoch,
            "after": start_epoch
        }
        resp = self.session.get(URL, headers=headers, params=params)
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
            resp = self.session.get(url, headers=headers, params=params)
            activity.set_streams(resp.json())
            activities_with_streams.append(activity)
        return activities_with_streams


