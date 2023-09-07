from fastapi import APIRouter
from app.adapters.strava_api_adapter import StravaAPIAdapter
from starlette.status import HTTP_200_OK
from models.activities import GetActivity
from typing import List


router = APIRouter()

@router.get(
    "activities/",
    response_model=List(GetActivity),
    name="strava:activities",
    status_code=HTTP_200_OK
)
async def get_strava_activities():
    adapter = StravaAPIAdapter()
    adapter.get_strava_athlete_activities()
