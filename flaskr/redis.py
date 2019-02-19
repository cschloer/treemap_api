import redis
from .settings import Settings

REDIS_HOST = Settings.get('REDIS_HOST')
REDIS_PORT = Settings.get('REDIS_PORT')
REDIS_PASSWORD = Settings.get('REDIS_PASSWORD')

redis = redis.StrictRedis(REDIS_HOST, REDIS_PORT, password=REDIS_PASSWORD, charset="utf-8", decode_responses=True)
