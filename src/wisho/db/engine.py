from functools import lru_cache

from sqlalchemy import Engine, create_engine

from wisho.settings import get_settings


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    engine = create_engine(
        url=settings.database.uri,
        echo=settings.database.echo,
        pool_pre_ping=settings.database.pool_pre_ping,
        pool_recycle=settings.database.pool_recycle,
        pool_size=settings.database.pool_size,
        max_overflow=settings.database.pool_max_overflow,
    )

    return engine
