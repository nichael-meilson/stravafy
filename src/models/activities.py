from models.core import IDModelMixin
import pydantic

class GetActivity(IDModelMixin):
    athlete_id: int = pydantic.Field(..., description="Internal Strava ID of the athlete.")
