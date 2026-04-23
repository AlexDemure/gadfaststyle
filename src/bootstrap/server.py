import asyncio
import contextlib
import typing

import uvicorn

from fastapi import Depends
from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.common.http.collections import HTTPHeader
from src.common.locales.utils import getlocale
from src.domain.collections import BusinessError
from src.entrypoints.http import router
from src.entrypoints.http.common.deps import basic
from src.entrypoints.http.common.deps import language
from src.framework.background import background
from src.framework.openapi import OpenAPI
from src.infrastructure.databases.postgres import postgres
from src.infrastructure.monitoring.asyncio.detector import detector
from src.infrastructure.monitoring.health import health
from src.infrastructure.monitoring.logging import logger
from src.infrastructure.storages.redis import redis
from src.localization import localization


@contextlib.asynccontextmanager
async def lifespan(_app: FastAPI) -> typing.Any:
    postgres.start()
    await redis.start()
    detector.start()
    background.start()
    logger.info("Application started")
    yield
    logger.info("Application shutdown")
    background.shutdown()
    detector.shutdown()
    await redis.shutdown()
    postgres.shutdown()


app = FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    dependencies=[Depends(language)],
)


@app.get(
    "/api/swagger",
    description="Swagger Documentation",
    include_in_schema=False,
    response_class=HTMLResponse,
    dependencies=[Depends(basic)],
)
def swagger() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/api/specification.json", title=app.title)


@app.get(
    "/api/redoc",
    description="Redoc Documentation",
    include_in_schema=False,
    response_class=HTMLResponse,
    dependencies=[Depends(basic)],
)
def redoc() -> HTMLResponse:
    return get_redoc_html(openapi_url="/api/specification.json", title=app.title)


@app.get(
    "/api/specification.json",
    description="API Specification",
    include_in_schema=False,
    response_model=dict,
    dependencies=[Depends(basic)],
)
def specification() -> dict[typing.Any, typing.Any]:
    return OpenAPI(app).generate()


@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, error: BusinessError) -> JSONResponse:
    locale = getlocale(request.headers.get(HTTPHeader.accept_language, "en"))
    translate = localization(locale)
    content = error.http
    content["detail"]["message"] = translate.errors[error.__class__.__name__]
    return JSONResponse(status_code=error.code, content=content)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, error: HTTPException) -> JSONResponse:
    locale = getlocale(request.headers.get(HTTPHeader.accept_language, "en"))
    translate = localization(locale)
    content: dict = {
        "status_code": error.status_code,
        "detail": {
            "type": str(error.status_code),
            "message": translate.http[error.status_code],
        },
    }
    return JSONResponse(status_code=error.status_code, content=content, headers=error.headers)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, error: RequestValidationError) -> JSONResponse:
    code = 422
    locale = getlocale(request.headers.get(HTTPHeader.accept_language, "en"))
    translate = localization(locale)
    message = translate.http[code]
    for err in error.errors():
        err["msg"] = message
    return JSONResponse(status_code=code, content={"status_code": code, "detail": error.errors()})


app.include_router(redis.router, dependencies=[Depends(basic)])

app.include_router(health.router)

app.include_router(router)

app.exclude_paths = []  # type: ignore

app.mount("/api/static", StaticFiles(directory="src/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def run() -> None:
    await uvicorn.Server(
        uvicorn.Config(
            app=app,
            host="0.0.0.0",
            port=8000,
            log_config=None,
        )
    ).serve()


if __name__ == "__main__":
    asyncio.run(run())
