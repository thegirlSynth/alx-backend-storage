#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""
from functools import wraps
import redis
import requests
import time
from typing import Callable

my_redis = redis.Redis()


def count_url(fn: Callable) -> Callable:
    """
    This decorator function keeps track of the number of times
    a url is accessed.
    """

    @wraps(fn)
    def wrapper(url: str):
        key = f"count:{url}"
        data = my_redis.get(key)

        if data:
            my_redis.incr(key)
            return data.decode("utf-8")

        my_redis.incr(key)
        my_redis.setex(key, 10, result)
        result = fn(url)

        return result

    return wrapper


@count_url
def get_page(url: str) -> str:
    """
    Tracks how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds.
    """

    response = requests.get(url)
    if response.status_code == 200:
        return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/"
    content = get_page(url)
    print(content)
