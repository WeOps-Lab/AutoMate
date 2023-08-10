class BlueException(Exception):

    ERROR_CODE = "0000000"
    MESSAGE = "APP异常"
    STATUS_CODE = 500

    def __init__(self, message=None, data=None, *args):
        """
        :param message: 错误消息
        :param data: 其他数据
        :param context: 错误消息 format dict
        :param args: 其他参数
        """
        super(BlueException, self).__init__(*args)
        self.message = self.MESSAGE if message is None else message
        self.data = data

    def render_data(self):
        return self.data

    def response_data(self):
        return {"result": False, "code": self.ERROR_CODE, "message": self.message, "data": self.render_data()}


class ClientBlueException(BlueException):

    MESSAGE = "客户端请求异常"
    ERROR_CODE = "40000"
    STATUS_CODE = 400


class ServerBlueException(BlueException):

    MESSAGE = "服务端服务异常"
    ERROR_CODE = "50000"
    STATUS_CODE = 500

    def __str__(self):
        return self.MESSAGE if getattr(self, "message", None) is None else self.message
