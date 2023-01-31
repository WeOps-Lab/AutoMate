from typing import Any, Optional

from pydantic import BaseModel


class CommonResponseSchema(BaseModel):
    message: Optional[str] = "success"
    result: bool = True
    data: Optional[Any] = None
