from interfaces.db import DB
from models.activities import Activities
from models.track import Tracks
from utils import read_config
import psycopg2
from typing import Dict

CONFIG = read_config()

class Postgres(DB):

    def __init__(self, params: Dict):
        self.connection: psycopg2.connection
        self.params: Dict = params

    def open_connection(self) -> None:
        self.connection = psycopg2.connect(**self.params)

    def close_connection(self) -> None:
        self.connection.close()

    def post_strava_activities(self, activities: Activities) -> None:
        pass

    def post_spotify_tracks(self, tracks: Tracks) -> None:
        pass

    


