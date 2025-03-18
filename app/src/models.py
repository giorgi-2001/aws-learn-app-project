from .database import Base, Mapped, mapped_column


class Image(Base):
    name: Mapped[str] = mapped_column(
        primary_key=True, unique=True, nullable=False
    )

    size: Mapped[int] = mapped_column(nullable=False)
    extension: Mapped[str] = mapped_column(nullable=False)
