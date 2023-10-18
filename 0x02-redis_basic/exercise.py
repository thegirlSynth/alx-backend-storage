#!/usr/bin/env python3
"""
Writing strings to Redis
"""

import redis
from typing import Union
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
