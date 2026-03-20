from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    role: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
