from fastapi import status
from .base import ServiceException
from ..common.messages import ERROR


class UserExistException(ServiceException):
    status_code = status.HTTP_409_CONFLICT
    message = ERROR["USER_EXIST"]


class UserConfirmedException(ServiceException):
    status_code = status.HTTP_409_CONFLICT
    message = ERROR["USER_CONFIRMED"]


class SendEmailException(ServiceException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = ERROR["SEND_EMAIL"]


class SendEmailTimeException(ServiceException):
    def __update_message(self):
        result = {}
        message = ERROR["SEND_EMAIL_TIME"]
        for lang in message.keys():
            result[lang] = message[lang].format(second=self.retry_time)
        return result

    def __init__(self, retry_time: int):
        self.retry_time = retry_time
        self.message = self.__update_message()

    status_code = status.HTTP_429_TOO_MANY_REQUESTS


class BlockedEmailException(ServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    message = ERROR["BLOCKED_EMAIL"]


class TokenException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = ERROR["INVALID_TOKEN"]


class TokenExpiredException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = ERROR["EXPIRED_TOKEN"]
    detail = {"isExpiredToken": True}


class UserNotExitException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = ERROR["USE_NOT_EXIT"]


class PasswordInvalidException(ServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = ERROR["PASSWORD_INVALID"]
