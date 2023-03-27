import typing

from pydantic import BaseModel, Field


class Inventory(BaseModel):
    host: str = Field("", description="主机")
    user: str = Field("", description="用户")
    password: str = Field("", description="密码")
    port: int = Field(22, description="端口")


class ADHocModel(BaseModel):
    module: str = Field("", description="模块名")
    module_args: str = Field("", description="模块参数,key=value")
    extra_vars: dict = Field({}, description="模块额外参数(dict)")
    inventory: typing.Union[typing.List[Inventory], None] = Field(None, description="主机清单")
    is_async: bool = Field(False, description="是否异步请求,默认同步")
    credential_id: str = Field("", description="凭据标识")
    timeout: typing.Union[None, int] = Field(None, description="超时时间,默认无")
