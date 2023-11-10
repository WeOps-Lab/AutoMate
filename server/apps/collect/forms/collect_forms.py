# -- coding: utf-8 --

# @File : collect_forms.py
# @Time : 2022/12/8 09:58
# @Author : windyzhao
import typing

from pydantic import BaseModel, Field


class CollectTaskModel(BaseModel):
    timeout: int = Field(0, description="超时时间")
    driver: str = Field("", description="能力")
    module: str = Field("", description="模块名")
    bk_obj_id: str = Field("", description="对象类型")
    classification: str = Field("", description="对象类型分类")
    credential: typing.List[str] = Field(..., description="凭据数组")
    context: dict = Field({}, description="业务额外参数")
