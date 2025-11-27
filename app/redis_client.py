try:
    import redis
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True
    )
except:
    redis_client = None

def get_redis():
    if redis_client is None:
        raise Exception("Redis not available")
    return redis_client
