from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    role: str
