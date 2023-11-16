from abc import ABC, abstractmethod
from models.activities import Activities
from models.track import Tracks
from typing import Dict
import psycopg2

@abs
class DB(ABC):
    connection: psycopg2.connection
    params: Dict

    @abstractmethod
    def open_connection(self) -> None:
        pass

    @abstractmethod
    def close_connection(self) -> None:
        pass

    @abstractmethod
    def post_strava_activities(self, activities: Activities) -> None:
        pass

    @abstractmethod
    def post_spotify_tracks(self, tracks: Tracks) -> None:
        pass

