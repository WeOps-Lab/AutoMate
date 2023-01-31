from typing import List

from pydantic import BaseModel, Field


class SshCommand(BaseModel):
    enable_mode: bool = Field(False, description="是否开启特权模式")
    host: str = Field("", description="网络设备IP")
    username: str = Field("", description="网络设备的SSH用户名")
    password: str = Field("", description="网络设备的SSH密码")
    secret: str = Field("", description="特权密码")
    port: int = Field(22, description="SSH端口")
    commands: List[str] = Field([], description="执行的指令")
    device_type: str = Field("", description="设备类型")
    timeout: int = Field(600, description="超时时间")
