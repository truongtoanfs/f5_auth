from httpx import Response
from .do_requests import BaseRequest
from config import ApiConfig


class Captcha(BaseRequest):

    def __init__(self):
        self.config = ApiConfig()

    def verify_recaptcha(self, ip: str, response: str):
        payload = {
            "remoteip": ip,
            "response": response,
            "secret": self.config.CAPTCHA_SECRET,
        }
        response: Response = self._do_request(
            method="post", url=self.config.CAPTCHA_URL, data=payload
        )
        verify_status = response.json()
        return verify_status["success"]
