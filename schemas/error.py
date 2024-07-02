from pydantic import BaseModel


class ErrorSchema(BaseModel):
    msg: str

