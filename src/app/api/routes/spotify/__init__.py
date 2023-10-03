from fastapi import APIRouter

from app.api.routes.spotify.tracks import router as tracks_router
from app.api.routes.spotify.auth import router as auth_router

router = APIRouter()
router.include_router(tracks_router)
router.include_router(auth_router)