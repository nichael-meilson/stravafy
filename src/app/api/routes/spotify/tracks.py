from fastapi import APIRouter
from app.adapters.spotify_api_adapter import SpotifyAPIAdapter
from starlette.status import HTTP_200_OK
from models.track import Tracks
from typing import List
import pydantic


router = APIRouter()

@router.get(
    "/tracks",
    response_model=Tracks,
    name="spotify:tracks",
    status_code=HTTP_200_OK
)
async def get_strava_activities(
    end_date: str
):
    adapter = SpotifyAPIAdapter()
    landed_tracks = adapter.get_recently_played_tracks(end=end_date)
    modelled_tracks = adapter.model_tracks(landed_tracks)
    tracks = adapter.get_track_metadata(modelled_tracks)
    return tracks

