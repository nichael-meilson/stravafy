from fastapi import APIRouter

from app.api.routes.landing import router as landing_router
from app.api.routes.strava_activities import router as activities_router
from app.api.routes.spotify_tracks import router as tracks_router

router = APIRouter()
router.include_router(landing_router)
router.include_router(activities_router)
router.include_router(tracks_router)