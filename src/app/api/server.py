from fastapi import FastAPI


def get_application():
    app = FastAPI()
    return app


app = get_application()