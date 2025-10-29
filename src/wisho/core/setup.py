from fastapi import APIRouter, FastAPI


def create_application(router: APIRouter) -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app
