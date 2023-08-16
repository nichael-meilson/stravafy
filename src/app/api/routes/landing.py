from fastapi import APIRouter
from starlette.status import HTTP_200_OK

router = APIRouter()

@router.get(
    "/",
    name="landing:get-landing",
    status_code=HTTP_200_OK,
)
async def get_landing():
    pass