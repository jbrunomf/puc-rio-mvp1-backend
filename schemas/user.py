from pydantic import BaseModel, PositiveInt


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
