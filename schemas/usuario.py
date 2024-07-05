from typing import List, Optional

from pydantic import BaseModel, PositiveInt


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    password_hash: Optional[str] = None


class UserListSchema(BaseModel):
    users: List[UserSchema]
