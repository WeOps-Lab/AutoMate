import typing

from pydantic import BaseModel, Field


class CloudReqModel(BaseModel):
    cloud_type: str = Field(description="操作类型,如aliyun,qcloud")
    operate_type: str = Field(description="操作类型,如list_vms")
    region: typing.Union[str, None] = Field(None, description="region")
    host: typing.Union[str, None] = Field(None, description="host")
    credential_id: typing.Union[str, None] = Field(None, description="凭据id")
    run_kwargs: typing.Dict = Field({}, description='执行参数,如{"param1":1,"param2":10}')


class CloudResultModel(BaseModel):
    result: bool = Field(True, description="执行是否成功")
    data: typing.Union[None, typing.List, typing.Dict] = Field(None, description="执行成功返回的JSON对象")
    message: str = Field("", description="执行的异常信息，success为False时可以使用此信息")
