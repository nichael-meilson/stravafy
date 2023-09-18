import pydantic
from typing import List, Dict, Double

class Track(pydantic.BaseModel):
    id: int = pydantic.Field(..., description="Internal Spotify ID of the track.")
    played_at: str = pydantic.Field(..., "Timestamp when track was played.")
    track_length: int = pydantic.Field(None, "Duration of track (in ms).")
    acousticness: float = pydantic.Field(None, "Acousticness rating (0-1.0).")
    danceability: float = pydantic.Field(None, "Danceability rating (0-1.0).")
    energy: float = pydantic.Field(None, "Energy rating (0-1.0).")
    instrumentalness: float = pydantic.Field(None, "Instrumentalness rating (0-1.0).")
    speechiness: float = pydantic.Field(None, "Speechiness rating (0-1.0).")
    tempo: float = pydantic.Field(None, "BPM of the track.")
    valence: float = pydantic.Field(None, "Percieved 'happiness' of the track.")

    
    def set_streams(self, streams: Dict):
        for key in ["heartrate", "time", "distance"]:
            if key in streams.keys():
                setattr(self, key, streams.get(key).get('data'))

            
    