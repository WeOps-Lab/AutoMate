from pydantic import BaseModel, Field


class AdHocResult(BaseModel):
    success: bool = Field(True, description="执行是否成功")
    result: dict = Field({}, description="执行AD-Hoc返回的JSON对象")
    message: str = Field("", description="执行的异常信息，success为False时可以使用此信息")
