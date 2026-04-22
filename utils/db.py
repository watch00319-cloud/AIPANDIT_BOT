"""
Database utilities for the Vedic Astrology Telegram bot.

Uses SQLAlchemy async with aiosqlite so no C/Rust toolchain is required.
The database file path is read from the DATABASE_URL environment variable
(defaults to sqlite+aiosqlite:///./bot_users.db next to main.py).
"""

import logging
import os
from typing import Optional

from sqlalchemy import BigInteger, Column, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Engine / session factory
# ---------------------------------------------------------------------------

DATABASE_URL: str = (
    os.getenv("DATABASE_URL") or "sqlite+aiosqlite:///./bot_users.db"
)

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# ---------------------------------------------------------------------------
# ORM model
# ---------------------------------------------------------------------------


class Base(DeclarativeBase):
    pass


class UserProfile(Base):
    """Persists basic user data collected during the consultation flow."""

    __tablename__ = "user_profiles"

    user_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(128), nullable=True)
    dob = Column(String(32), nullable=True)   # date of birth  (YYYY-MM-DD)
    tob = Column(String(16), nullable=True)   # time of birth  (HH:MM)
    place = Column(String(256), nullable=True)
    language = Column(String(16), nullable=True, default="hi")
    notes = Column(Text, nullable=True)


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


async def init_db() -> None:
    """Create all tables if they do not already exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialised (tables created / verified).")


async def get_profile(user_id: int) -> Optional[UserProfile]:
    """Return the UserProfile for *user_id*, or None if not found."""
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        result = await session.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()


async def upsert_profile(user_id: int, **kwargs) -> UserProfile:
    """Create or update a UserProfile row for *user_id*.

    Keyword arguments map directly to UserProfile columns, e.g.::

        await upsert_profile(user_id, name="Arjun", dob="1990-05-15")
    """
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        result = await session.execute(
            select(UserProfile).where(UserProfile.user_id == user_id)
        )
        profile: Optional[UserProfile] = result.scalar_one_or_none()

        if profile is None:
            profile = UserProfile(user_id=user_id, **kwargs)
            session.add(profile)
        else:
            for key, value in kwargs.items():
                setattr(profile, key, value)

        await session.commit()
        await session.refresh(profile)
        return profile
