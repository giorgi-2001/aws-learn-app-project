from datetime import datetime

from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncAttrs
)
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from .config import DB_URL


engine = create_async_engine(DB_URL)


SessionLocal = async_sessionmaker(bind=engine)


class Base(DeclarativeBase, AsyncAttrs):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"
    
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )

    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now, onupdate=datetime.now
    )