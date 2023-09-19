import pydantic
from typing import List, Dict

class Track(pydantic.BaseModel):
    id: str = pydantic.Field(..., description="Internal Spotify ID of the track.")
    title: str = pydantic.Field(..., description="Track title.")
    artist: List[str] = pydantic.Field(..., description="Track artist.")
    album: str = pydantic.Field(..., description="Track album.")
    release_date: str = pydantic.Field(..., description="Track release year.")
    played_at: str = pydantic.Field(..., description="Timestamp when track was played.")
    track_length: int = pydantic.Field(..., description="Duration of track (in ms).")
    acousticness: float = pydantic.Field(None, description="Acousticness rating (0-1.0).")
    danceability: float = pydantic.Field(None, description="Danceability rating (0-1.0).")
    energy: float = pydantic.Field(None, description="Energy rating (0-1.0).")
    instrumentalness: float = pydantic.Field(None, description="Instrumentalness rating (0-1.0).")
    speechiness: float = pydantic.Field(None, description="Speechiness rating (0-1.0).")
    tempo: float = pydantic.Field(None, description="BPM of the track.")
    valence: float = pydantic.Field(None, description="Percieved 'happiness' of the track.")

    
    def set_features(self, features: Dict, feature_titles: List):
        for key in feature_titles:
            if key in features.keys():
                setattr(self, key, features.get(key))

            
    