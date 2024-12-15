from typing import Union
from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI()


class Factory:
    def create_app(self, config):
        app = FastAPI()
        app.include_router(api_router)
        return app