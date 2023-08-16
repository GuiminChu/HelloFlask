from enum import Enum
from flask import jsonify


class _ResponseCode(Enum):
    SUCCESS = 200
    FAILURE = 400


class _ResponseMessage(Enum):
    SUCCESS = "操作成功"
    FAILURE = "操作失败"
    DEFAULT_NULL_MESSAGE = "暂无承载数据"


class RP(object):
    """
    统一 API 响应结果封装
    """

    def __init__(self, code: int, data, msg: str):
        self.code = code
        self.data = data
        self.msg = msg

    @classmethod
    def success(cls, msg: str):
        return jsonify(cls(_ResponseCode.SUCCESS.value, None, msg).__dict__)

    @classmethod
    def fail(cls, msg: str):
        return jsonify(cls(_ResponseCode.FAILURE.value, None, msg).__dict__)

    @classmethod
    def data(cls, data):
        return jsonify(cls(_ResponseCode.SUCCESS.value, data, _ResponseMessage.SUCCESS.value).__dict__)

    # @classmethod
    # def data(cls, data, msg: str):
    #     return cls(_ResponseCode.SUCCESS.value, data, msg).__dict__

    @classmethod
    def status(cls, flag: bool):
        if flag:
            return jsonify(cls.success(_ResponseMessage.SUCCESS.value))
        else:
            return jsonify(cls.fail(_ResponseMessage.FAILURE.value))
