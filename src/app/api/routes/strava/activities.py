from fastapi import APIRouter
from app.adapters.strava_api_adapter import StravaAPIAdapter
from starlette.status import HTTP_200_OK
from models.activities import Activities


router = APIRouter()

@router.get(
    "/activities",
    response_model=Activities,
    name="strava:activities",
    status_code=HTTP_200_OK
)
async def get_strava_activities(
    start_date: str,
    end_date: str
):
    adapter = StravaAPIAdapter()
    result_activities = Activities()
    landed_activities = adapter.get_strava_activities(start_date, end_date)
    modelled_activities = adapter.model_strava_activities(landed_activities)
    clean_activities = adapter.get_strava_activity_streams(modelled_activities)
    result_activities.set_activities(clean_activities)
    return result_activities

