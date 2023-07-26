from .handler import env


REDIS_USER = env.str("REDIS_USER", "default")
REDIS_PASSWORD = env.str("REDIS_PASSWORD", "foobared")
REDIS_HOST = env.str("REDIS_HOST", "localhost")
REDIS_PORT = env.str("REDIS_PORT", "6379")

REDIS_CONNECTION_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CONNECTION_URI,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": False,
        },
        "KEY_FUNCTION": "apps.core.redis.make_key",
        "KEY_PREFIX": "BISTI",
        "VERSION": 1,
    }
}

if REDIS_PASSWORD:
    CACHES["default"]["OPTIONS"]["PASSWORD"] = REDIS_PASSWORD
    REDIS_CONNECTION_URI = (
        f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    )
    CACHES["default"]["LOCATION"] = REDIS_CONNECTION_URI
