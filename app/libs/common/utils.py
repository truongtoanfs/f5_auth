from ..exception.service import BlockedEmailException


def check_black_domain(email: str):
    with open("app/libs/disposable_email_blocklist.conf") as blocklist:
        blocklist_content = {line.rstrip() for line in blocklist.readlines()}
        if email.partition("@")[2] in blocklist_content:
            raise BlockedEmailException
