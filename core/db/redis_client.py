from redis import StrictRedis

from core.settings import settings

get_redis_client = lambda redis_url: StrictRedis.from_url(redis_url, encoding="utf8", decode_responses=True)  # noqa
redis_client = get_redis_client(settings.redis_url)
