from datetime import datetime

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    role: str


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
