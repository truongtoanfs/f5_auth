from .base import ServiceException
from ..common.messages import ERROR


class UserExistException(ServiceException):
    status_code = 409
    detail = ERROR["USER_EXIST"]


class UserConfirmedException(ServiceException):
    status_code = 400
    detail = ERROR["USER_CONFIRMED"]
