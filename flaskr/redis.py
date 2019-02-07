import redis
from .settings import Settings

REDIS_HOST = Settings.get('REDIS_HOST')
REDIS_PORT = Settings.get('REDIS_PORT')

redis = redis.StrictRedis(REDIS_HOST, REDIS_PORT, charset="utf-8", decode_responses=True)
