from redis import StrictRedis

get_redis_client = lambda redis_url: StrictRedis.from_url(redis_url, encoding="utf8", decode_responses=True)  # noqa
"""
使用上下文管理器,及时释放redis
with get_redis_client(settings.redis_url) as redis_client:
    redis_client.xx()
"""
