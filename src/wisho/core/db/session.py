from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from wisho.core.config import get_settings

settings = get_settings()

async_engine = create_async_engine(
    settings.database.uri,
    echo=settings.database.echo,
    future=settings.database.future,
)

local_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=settings.database.expire_on_commit,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with local_session() as session:
        yield session
