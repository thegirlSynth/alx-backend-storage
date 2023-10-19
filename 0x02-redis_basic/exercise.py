#!/usr/bin/env python3
"""
Writing strings to Redis
"""

import redis
from typing import Callable, Optional, Union
import uuid


class Cache:
    def __init__(self):
        """
        Initializes the Cache class by storing an instance
        of the Redis client as a private variable named _redis
        """

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores input data in Redis using the random key and returns the key.
        """

        r_key = str(uuid.uuid4())
        self._redis.set(r_key, data)
        return r_key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """
        Takes a string argument and an optional Callable argument
        that converts the data back to the desired format.
        """
        value = self._redis.get(key)
        if value:
            if fn:
                value = fn(value)
        return value

    def get_str(self, key: str) -> Union[str, bytes, int, float]:
        """
        Automatically parameterizes Cache.get with the conversion function
        for strings.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[str, bytes, int, float]:
        """
        Automatically parameterizes Cache.get with the conversion function
        for ints.
        """
        return self.get(key, int)
