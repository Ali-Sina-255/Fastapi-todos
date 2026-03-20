from pydantic import BaseModel, Field

from datetime import datetime

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
        from_attributes = True