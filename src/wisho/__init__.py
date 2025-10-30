import uvicorn

from wisho.api import router
from wisho.core.config import get_settings
from wisho.core.setup import create_application

app = create_application(router)


def main() -> None:
    settings = get_settings()

    uvicorn.run(
        "wisho:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
