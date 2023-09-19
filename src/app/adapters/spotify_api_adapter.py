import requests
from src.utils import read_config
from src.utils.encryption import Encryption
from src.utils.spotify_auth_handler import SpotifyAuthHandler
from src.models.track import Track
import webbrowser
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
        
    def get_recently_played_tracks(self, start: int, end: int) -> List:
        """
        start: epoch timestamp
        end: epoch timestamp
        """
        url = "https://api.spotify.com/v1/me/player/recently-played"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "after": start
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







