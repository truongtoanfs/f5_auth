import json
from ..common.messages import ERROR


class BaseException(Exception):
    status_code = 500
    detail = ERROR["GENERAL"]

    def output(self):
        data = {
            "status_code": self.status_code,
            "detail": self.detail,
        }
        return data

    def __str__(self):
        return json.dumps(self.output())


class ServiceException(BaseException): ...
