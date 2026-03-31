import uuid
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID]  = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    title: Mapped[str] =mapped_column(String(255), nullable=False) 
    completed: Mapped[bool] = mapped_column(nullable=False,default=False) 
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
