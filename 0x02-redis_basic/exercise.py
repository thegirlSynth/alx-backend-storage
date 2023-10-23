#!/usr/bin/env python3
"""
Writing strings to Redis
"""

from functools import wraps
import redis
from typing import Callable, Optional, Union
import uuid


def count_calls(method: Callable) -> Callable:
    """
    This decorator function keeps track of the number of times
    a function is called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    This decorator function stores the history of inputs and outputs
    for a particular function.
    """
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args):
        self._redis.rpush(input_key, str(args))
        result = method(self, str(args))
        self._redis.rpush(output_key, str(result))
        return result

    return wrapper


class Cache:
    def __init__(self):
        """
        Initializes the Cache class by storing an instance
        of the Redis client as a private variable named _redis
        """

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

    def replay(self, fn):
        """
        Displays the history of calls of a particular function.
        """
        ins = self._redis.lrange("{}:inputs".format(fn.__qualname__), 0, -1)
        outs = self._redis.lrange("{}:outputs".format(fn.__qualname__), 0, -1)

        print(f"Cache.store was called {len(ins)} times:")
        for i in range(len(ins)):
            input = ins[i].decode("utf-8")
            output = outs[i].decode("utf-8")
            print(f"Cache.store(*{str(input)}) -> {str(output)}")
