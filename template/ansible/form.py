from pydantic import BaseModel

from core.http_schemas.common_response_schema import CommonResponseSchema


class RequestModel(BaseModel):
    pass


class ResultModel(BaseModel):
    pass


class ResponseModel(CommonResponseSchema):
    result: ResultModel = ResultModel()
