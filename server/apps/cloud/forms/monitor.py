import typing

from pydantic import BaseModel, Field


class ResourceModel(BaseModel):
    bk_obj_id: str = Field(description="CMDB 模型ID")
    bk_inst_id: int = Field(description="CMDB 实例ID")
    bk_inst_name: str = Field(description="CMDB 实例名")
    resource_id: str = Field(description="CMDB `resource_id` 属性")
    bk_biz_id: int = Field(0, description="CMDB 业务ID,默认0")


class MonitorReqModel(BaseModel):
    cloud_type: str = Field(description="操作类型,如aliyun,qcloud")
    host: typing.Union[str, None] = Field("", description="主机IP,如127.0.0.1")
    region: typing.Union[str, None] = Field("", description="区域Region,如a.b")
    resources: typing.List[ResourceModel] = Field([], description="资源列表")
    start_time: typing.Union[str, None] = Field(None, description="起始时间 如2022-12-12 14:10:00")
    end_time: typing.Union[str, None] = Field(None, description="结束时间 2022-12-12 14:15:00")
    metrics: typing.List[str] = Field([], description='指标列表,如["CPUUsage","MemUsed","MemUsage"]')
    period: int = Field(300, description="间隔时间,默认5分钟300s")
    credential_id: typing.Union[str, None] = Field(None, description="凭据id")


class DimensionModel(BaseModel):
    name: str = Field("", description="维度名,如 `挂载点`")
    key: str = Field(description="维度Key,如 `mount_point`")
    value: str = Field("", description="维度值 `/data`,")


class MetricModel(BaseModel):
    name: typing.Optional[str] = Field(None, description="指标名,如`CPU使用率`")
    key: str = Field(description="指标Key,如`CpuUsage`")
    value: float = Field(description="指标值(浮点型)")
    dims: typing.Optional[typing.List[DimensionModel]] = Field(None, description="指标维度[列表]")
    bk_biz_id: typing.Optional[int] = Field(None, description="CMDB业务ID,如2(蓝鲸)")
    protocol: str = Field(None, description="CMDB模型分组,如database")
    bk_obj_id: str = Field(description="CMDB模型ID,如mysql")
    bk_inst_id: typing.Optional[int] = Field(None, description="CMDB实例ID,如10")
    bk_inst_name: typing.Optional[str] = Field(None, description="CMDB实例名,如mysql-1")
    resource_id: typing.Optional[str] = Field(None, description="资产名,如234")
