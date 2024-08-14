#!/usr/bin/env python3
"""Redis client module"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional, Any


class Cache:
    """Caching class"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store the input data in redis and
        return the randomly generated key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> None:
        """
        retrieve data from redis and apply an optional conversion function
        """
        client = self._redis
        value = client.get(key)
        if not value:
            return
        if fn is int:
            return self.get_int(value)
        if fn is str:
            return self.get_str(value)
        if Callable(fn):
            return fn(value)

    def get_str(self, key: str) -> Optional(str):
        """
        retrieve a string from redis and decode it using UTF-8
        """
        return data.decode('UTF-8')

    def get_int(self, data: bytes) -> int:
        """
        retrieves an integer from redis
        """
        return int(data)
