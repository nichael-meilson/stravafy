from fastapi import APIRouter

from app.api.routes.landing import router as landing_router
from app.api.routes.strava_activities import router as activities_router

router = APIRouter()
router.include_router(landing_router)
router.include_router(activities_router)