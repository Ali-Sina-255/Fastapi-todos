# apps/models/models.py
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from apps.config.db import Base
from pydantic import BaseModel, Field
from datetime import datetime

# ================= SQLAlchemy model =================
class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    priority = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

# ================= Pydantic request schema =================
class TodoRequestSchema(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(max_length=255)
    is_completed: bool
    priority: int = Field(gt=0, lt=6)

# ================= Pydantic response schema =================
class TodoResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
    priority: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # 🔥 important for SQLAlchemy objects