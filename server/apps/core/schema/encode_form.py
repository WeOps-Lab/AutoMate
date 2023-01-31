from pydantic import BaseModel


class EncodeForm(BaseModel):
    content: str
