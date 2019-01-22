import redis

redis = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
