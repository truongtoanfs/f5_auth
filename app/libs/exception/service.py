from .base import ServiceException
from ..common.messages import ERROR


class UserExistException(ServiceException):
    status_code = 409
    detail = ERROR["USER_EXIST"]


class UserConfirmedException(ServiceException):
    status_code = 400
    detail = ERROR["USER_CONFIRMED"]


class SendEmailException(ServiceException):
    status_code = 500
    detail = ERROR["SEND_EMAIL"]


class BlockedEmailException(ServiceException):
    status_code = 403
    detail = ERROR["BLOCKED_EMAIL"]
