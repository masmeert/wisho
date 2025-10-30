from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from wisho.core.config import get_settings


def create_application(router: APIRouter) -> FastAPI:
    settings = get_settings()

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app
