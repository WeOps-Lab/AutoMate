from pydantic import BaseModel


class DecodeForm(BaseModel):
    content: str
