from fastapi import Request
from ..exception.service import BlockedEmailException
from datetime import datetime


def check_black_domain(email: str):
    with open("app/libs/disposable_email_blocklist.conf") as blocklist:
        blocklist_content = {line.rstrip() for line in blocklist.readlines()}
        if email.partition("@")[2] in blocklist_content:
            raise BlockedEmailException


def get_language(request: Request):
    accept_language = request.headers.get("accept-language")
    if accept_language and "en" in accept_language:
        return "en"
    return "vi"


def seconds_left():
    now = datetime.now()
    end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)
    time_left = end_of_day - now
    return int(time_left.total_seconds())
