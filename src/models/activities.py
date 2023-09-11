from models.core import IDModelMixin
import pydantic

class GetActivity(IDModelMixin):
    athlete_id: int = pydantic.Field(..., description="Internal Strava ID of the athlete.")
    start_date: str = pydantic.Field(..., description="Start datetime of the activity.")
    start_date_local: str = pydantic.Field(..., description="Local start datetime of the activity.") # Not sure which one I'll have to use
    activity_id: int = pydantic.Field(..., description="Internal Strava ID of the activity.")
