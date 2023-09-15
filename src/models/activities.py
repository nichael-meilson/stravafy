import pydantic
from typing import List, Dict

class Activity(pydantic.BaseModel):
    id: int = pydantic.Field(..., description="Internal Strava ID of the activity.")
    athlete_id: int = pydantic.Field(..., description="Internal Strava ID of the athlete.")
    activity_type: str = pydantic.Field(..., description="Type of activity (run, bike, swim, etc...).")
    timezone: str = pydantic.Field(..., description="Timezone activity took place in.")
    start_date: str = pydantic.Field(..., description="Start datetime (UTC) of the activity.")
    suffer_score: int = pydantic.Field(..., description="Suffer score of the activity.")
    heartrate: List[int] = pydantic.Field(None, description="Stream data of heart rate (BPM).")
    time: List[int] = pydantic.Field(None, description="Stream data of time of activity (Seconds).")
    distance: List[int] = pydantic.Field(None, description="Stream data of distance of activity (Metres).")
    
    def set_streams(self, streams: Dict):
        for key in ["heartrate", "time", "distance"]:
            if key in streams.keys():
                setattr(self, key, streams.get(key).get('data'))

            
    