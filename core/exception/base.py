from starlette.exceptions import HTTPException


class AutoMateException(HTTPException):
    ERROR_CODE = "000000"
    MESSAGE = "APP异常"
    STATUS_CODE = 500

    def __init__(self, msg="", status_code=0, error_code="", data: dict = None):
        self.message = detail = msg or self.MESSAGE
        status_code = status_code or self.STATUS_CODE
        super(AutoMateException, self).__init__(status_code, detail)
        self.error_code = error_code or self.ERROR_CODE
        self.data = data or {}

    def render_data(self):
        return self.data

    def response_data(self):
        return {"result": False, "code": self.error_code, "message": self.message, "data": self.render_data()}


class ClientError(AutoMateException):
    ERROR_CODE = "400000"
    MESSAGE = "客户端异常"
    STATUS_CODE = 400


class ServerError(AutoMateException):
    ERROR_CODE = "500000"
    MESSAGE = "服务器异常"
    STATUS_CODE = 500


class ParamValidationError(ClientError):
    ERROR_CODE = "400001"
    MESSAGE = "参数校验失败"


class CredentialNotFound(ClientError):
    ERROR_CODE = "400201"
    MESSAGE = "凭据不存在"


class DriverError(ServerError):
    ERROR_CODE = "500200"
    MESSAGE = "驱动异常"


class AnsibleRunnerError(DriverError):
    ERROR_CODE = "500201"
    MESSAGE = "Ansible执行异常"


class FormatError(ServerError):
    ERROR_CODE = "500300"
    MESSAGE = "数据转换失败"
