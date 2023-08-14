from fastapi import APIRouter
from app.adapters.fastapi_adapter import init_app
from app.core.use_cases import ExampleUseCase

router = APIRouter()
app = init_app()

@router.get("/")
async def read_root():
    use_case = ExampleUseCase()
    result = use_case.execute()
    return result
