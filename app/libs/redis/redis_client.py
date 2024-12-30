import redis
from config import apiConfig


class RedisClient:
    def __init__(self):
        self.redis_conn = redis.Redis(
            host=apiConfig.REDIS_HOST,
            port=apiConfig.REDIS_PORT,
            decode_responses=True,
        )

    def get(self, key: str):
        return self.redis_conn.get(key)

    def set(self, key: str, value: str):
        return self.redis_conn.set(key, value)


# redis_client = RedisClient()

# result = redis_client.set(key="age", value=12)
# username = redis_client.get(key="name")
