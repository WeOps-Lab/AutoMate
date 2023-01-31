import typing

from pydantic import BaseModel, Field


class TaskModel(BaseModel):
    task_id: typing.Union[str, typing.List[str]] = Field(description="任务uuid或uuid列表")


class TaskListModel(BaseModel):
    status: typing.Union[None, typing.List[str]] = Field(default=None, description="状态列表,如['STARTED','SUCCESS']")
