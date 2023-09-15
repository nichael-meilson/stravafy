import requests
from src.utils import read_config
from src.utils.encryption import Encryption

class SpotifyAPIAdapter:
    client_id: str
    session: requests.Session
    access_token: str

    def __init__(self) -> None:
        config = read_config()
        self.client_id: str = Encryption().decrypt_string(config["spotify_credentials"]["client_id"])
        self.session: requests.Session = requests.session()
        self.access_token: str = self.authorize_strava_api()