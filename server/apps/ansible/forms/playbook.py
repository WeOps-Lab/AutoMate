from pydantic import BaseModel, Field


class PlaybookModel(BaseModel):
    playbook_name: str = Field(description="playbook名字")
    extra_vars: dict = Field(description="playbook 变量字典")
