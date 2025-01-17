import time
from functools import wraps
import httpx


def request_connection_handler(max_retry=2):
    def decorator(func):
        @wraps(func)
        def handle(*args, **kwargs):
            retry_count = 0
            error = None
            while retry_count < max_retry:
                try:
                    response = func(*args, **kwargs)
                    return response
                except httpx.HTTPError as e:
                    error = e
                    retry_count += 1
                    time.sleep(retry_count)  # Exponential backoff for retries
            raise error

        return handle

    return decorator


class BaseRequest:
    @request_connection_handler()
    def _do_request(self, method, url, timeout=60, **kwargs):
        with httpx.Client() as client:
            method_handler = getattr(client, method, None)
            if method_handler is None:
                raise ValueError(f"Invalid HTTP method: {method}")

            response = method_handler(url, timeout=timeout, **kwargs)
            return response
