import string
import secrets
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthHandler:

    def generate_random_password(password_length: int = 12):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        while True:
            password = "".join(secrets.choice(alphabet) for i in range(password_length))
            if (
                any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3
                and any(c in string.punctuation for c in password)
            ):
                break

    def generate_hash_password(password: str):
        return pwd_context.hash(password)

    def verify_hash_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
