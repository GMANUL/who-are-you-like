from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from settings.settings import settings


def sqlite_connection() -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(f"sqlite+aiosqlite:///{settings.paths.database}", connect_args={"check_same_thread": False})

    return async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
