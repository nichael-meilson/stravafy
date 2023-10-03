from fastapi import APIRouter

from app.api.routes.landing import router as landing_router
from app.api.routes.strava import router as strava_router
from app.api.routes.spotify import router as spotify_router

router = APIRouter()
router.include_router(landing_router)
router.include_router(strava_router)
router.include_router(spotify_router)