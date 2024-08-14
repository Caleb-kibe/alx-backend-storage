#!/usr/bin/env python3
"""Redis client module"""

import redis
from uuid import uuid4
from typing import Any, Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """docorator that counts the number of times a function is called"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Incrememt the counter for the method using its qualified name
        key = f"{method.__qualname__}_calls"
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history() -> Callable:
    """
    decorator that stores the history of inputs and outputs for a function
    """
    def wrapper(self, *args, **kwargs):
        # creates keys for storing the input and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{methods.__qualname__}:outputs"

        # store input arguments as as a string in the input list
        self._redis.rpush(input_key, str(args))

        # execute the originall function and store its output
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


class Cache:
    """Caching class"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store the input data in redis and
        return the randomly generated key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
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
        if callable(fn):
            return fn(value)

    def get_str(self, data: bytes) -> Optional[str]:
        """
        retrieve a string from redis and decode it using UTF-8
        """
        return data.decode('UTF-8')

    def get_int(self, data: bytes) -> int:
        """
        retrieves an integer from redis
        """
        return int(data)
