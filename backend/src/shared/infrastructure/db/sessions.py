from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from shared.infrastructure.db import engines


postgres_session_factory = sessionmaker(  # type: ignore[call-overload]
    engines.postgres_engine,
    class_=AsyncSession,
)
