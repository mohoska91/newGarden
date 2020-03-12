from json import dumps, loads

import redis


class GpioCache:

    _GPIO_CACHE_KEY = "gpio cache"

    def __init__(self):
        self._redis = redis.Redis("configdb")
        cache = self._redis.get(self._GPIO_CACHE_KEY)
        self._cache = (cache and loads(cache)) or {}

    def is_in_cache(self, gpio: int):
        return str(gpio) in self._cache

    def get_status(self, gpio: int):
        return bool(self._cache.get(gpio))

    def put_in_cache(self, gpio: int, status: bool):
        self._cache[gpio] = int(status)
        self._syncronize()

    def remove_from_cache(self, gpio: int):
        self._cache.pop(gpio)
        self._syncronize()

    def remove_all_from_cache(self):
        self._redis.delete(self._GPIO_CACHE_KEY)

    def _syncronize(self):
        self._redis.set(self._GPIO_CACHE_KEY, dumps(self._cache))
