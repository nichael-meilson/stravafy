from fastapi import APIRouter

from app.api.routes.landing import router as landing_router
from app.api.routes.strava import router as strava_router
from app.api.routes.spotify.tracks import router as tracks_router

router = APIRouter()
router.include_router(landing_router)
router.include_router(strava_router)
router.include_router(tracks_router)