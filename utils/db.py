import os
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import Integer, String, Float, DateTime, Text, select, Boolean
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Overridable via env so a Railway persistent volume can be mounted at e.g.
# /data and DATABASE_URL set to "sqlite+aiosqlite:////data/bot_users.db".
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot_users.db")


class Base(DeclarativeBase):
    pass


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True, nullable=False)

    name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    dob: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    tob: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    place: Mapped[Optional[str]] = mapped_column(String(160), nullable=True)
    lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    lon: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    horoscope_subscribed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    q1: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    q2: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    q3: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    q4: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    q5: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


engine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_profile(user_id: int) -> Optional[UserProfile]:
    async with SessionLocal() as session:
        result = await session.execute(select(UserProfile).where(UserProfile.user_id == user_id))
        return result.scalar_one_or_none()


async def upsert_profile(user_id: int, data: Dict[str, Any]) -> UserProfile:
    async with SessionLocal() as session:
        result = await session.execute(select(UserProfile).where(UserProfile.user_id == user_id))
        profile = result.scalar_one_or_none()

        if profile is None:
            profile = UserProfile(user_id=user_id, **data)
            session.add(profile)
        else:
            for key, value in data.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)

        await session.commit()
        await session.refresh(profile)
        return profile


async def get_subscribed_users() -> list[UserProfile]:
    async with SessionLocal() as session:
        result = await session.execute(
            select(UserProfile).where(UserProfile.horoscope_subscribed == True)
        )
        return list(result.scalars().all())


async def save_answers(user_id: int, answers: Dict[str, str]) -> UserProfile:
    return await upsert_profile(user_id, answers)
