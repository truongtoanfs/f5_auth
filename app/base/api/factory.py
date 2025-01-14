from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse
from app.api import router as api_router
from config import ApiConfig
from app.libs.exception.base import ServiceException, BaseException
from app.libs.common.utils import get_language


class Factory:
    def create_app(self, config: ApiConfig):
        app = FastAPI(
            title=config.TITLE,
            version=config.VERSION,
            contact=config.CONTACT,
            docs_url=config.DOC_URL,
        )

        @app.exception_handler(Exception)
        def handle_error(request: Request, e: Exception):
            if isinstance(e, HTTPException):
                status_code = e.status_code
                data = dict(message=e.detail, status_code=status_code)
            elif isinstance(e, BaseException):
                status_code = e.status_code
                data = e.output()
                data["message"] = data["message"][get_language(request)]
            else:
                service_error = ServiceException()
                data = service_error.output()
                status_code = data["status_code"]
                data["message"] = data["message"][get_language(request)]
            response = JSONResponse(status_code=status_code, content=data)
            return response

        app.include_router(api_router)

        return app
