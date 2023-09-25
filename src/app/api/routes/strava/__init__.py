from fastapi import APIRouter

from app.api.routes.strava.activities import router as activities_router
from app.api.routes.strava.auth import router as auth_router

router = APIRouter()
router.include_router(activities_router)
router.include_router(auth_router)