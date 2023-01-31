from pydantic import Field
from pydantic.main import BaseModel


class CredentialRequestModel(BaseModel):
    credential_id: str = Field("", description="凭据路径")


class CommonAnsibleResultModel(BaseModel):
    changed: bool = Field(False, description="是否变更")
