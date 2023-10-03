import requests
from utils import read_config, convert_string_date_to_epoch
import os
from utils.encryption import Encryption
from utils.spotify_auth_handler import SpotifyAuthHandler
from models.track import Track
from selenium import webdriver
from starlette.exceptions import HTTPException
from typing import List

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
        """
        Only works after the user has called the /auth/strava endpoint
        Only works if STRAVA_ACCESS_TOKEN is in an env var
        """
        access_token = os.environ.get("SPOTIFY_ACCESS_TOKEN")
        if access_token:
            return access_token
        else:
            raise "No auth token returned - did the user authorize Spotify?"
        
    def get_recently_played_tracks(self, end: str) -> List:
        """
        start: string timestamp "YYYY-mm-dd"
        end: string timestamp "YYYY-mm-dd"
        """
        url = "https://api.spotify.com/v1/me/player/recently-played"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "after": convert_string_date_to_epoch(end)
        }
        resp = self.session.get(url, headers=headers, params=params)
        return resp.json()

    def model_tracks(self, tracks: List) -> List[Track]:
        track_list = []
        for track in tracks['items']:
            modelled_track = Track(
                id=track["track"]["id"],
                title=track["track"]["name"],
                artist=[artist["name"] for artist in track["track"]["artists"]],
                album=track["track"]["album"]["name"],
                release_date=track["track"]["album"]["release_date"],
                played_at=track["played_at"],
                track_length=track["track"]["duration_ms"]
            )
            track_list.append(modelled_track)
        return track_list
    
    def get_track_metadata(self, tracks: List[Track]) -> List[Track]:
        """
        Add metadata to tracks
        """
        tracks_with_metadata = []
        metadata_features = ["acousticness","danceability","energy","instrumentalness","speechiness","tempo","valence"]
        ids = []
        for track in tracks:
            ids.append(track.id)
        url = "https://api.spotify.com/v1/audio-features"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"ids": str(ids).replace("[","").replace("]","").replace("'","").replace(" ","")}
        resp = self.session.get(url, headers=headers, params=params)
        data = resp.json()
        for features in data["audio_features"]:
            for track in tracks:
                if features["id"] == track.id:
                    track.set_features(features, metadata_features)
                    tracks_with_metadata.append(track)
        
        return tracks_with_metadata







