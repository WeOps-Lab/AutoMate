from pydantic import BaseModel, Field


class NetworkSshResult(BaseModel):
    command_result: dict = Field({})
    err_message: str = Field("")
