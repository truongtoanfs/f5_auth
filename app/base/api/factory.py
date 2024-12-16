from fastapi import FastAPI
from app.api import router as api_router
from config import ApiConfig
app = FastAPI()


class Factory:
    def create_app(self, config: ApiConfig):
        app = FastAPI(
            title=config.TITLE,
            version=config.VERSION,
            contact=config.CONTACT,
            docs_url=config.DOC_URL,
        )
        app.include_router(api_router)
        return app