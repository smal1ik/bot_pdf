from typing import List, Any, Optional, Set

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Interval
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from decouple import config

engine = create_async_engine(config('POSTGRESQL'), echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    subscribed: Mapped[bool] = mapped_column(Boolean, default=False)
    click_id: Mapped[str] = mapped_column(nullable=True)
