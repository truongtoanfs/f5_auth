import json
from ..common.messages import ERROR


class BaseException(Exception):
    status_code = 500
    message = ERROR["GENERAL"]
    detail = None

    def output(self):
        data = {
            "status_code": self.status_code,
            "message": self.message,
        }
        if self.detail:
            data["detail"] = self.detail
        return data

    def __str__(self):
        return json.dumps(self.output())


class ServiceException(BaseException): ...
