from fastapi import status
from .base import ServiceException
from ..common.messages import ERROR


class UserExistException(ServiceException):
    status_code = status.HTTP_409_CONFLICT
    detail = ERROR["USER_EXIST"]


class UserConfirmedException(ServiceException):
    status_code = status.HTTP_409_CONFLICT
    detail = ERROR["USER_CONFIRMED"]


class SendEmailException(ServiceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ERROR["SEND_EMAIL"]


class BlockedEmailException(ServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = ERROR["BLOCKED_EMAIL"]


class TokenException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ERROR["INVALID_TOKEN"]


class UserNotExitException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ERROR["USE_NOT_EXIT"]


class PasswordInvalidException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = ERROR["PASSWORD_INVALID"]
