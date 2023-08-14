from fastapi import FastAPI
from app.interfaces.web.routes import router

def init_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app
