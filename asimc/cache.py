from collections import OrderedDict
import threading

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.lock = threading.Lock()
        self.capacity = capacity

    def get(self, key) -> int:
        with self.lock:
            if key not in self.cache:
                return -1
            value = self.cache.pop(key)
            self.cache[key] = value  # 移动到末尾表示最近使用
            return value

    def put(self, key, value) -> None:
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)  # 如果已经存在，则移动到末尾
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False)  # 弹出最老的项


def lru_cache(capacity: int):
    cache = LRUCache(capacity)

    def decorator(func):
        def wrapper(*args, **kwargs):
            key = (
                str(args),
                str(kwargs),
            )  # Use a tuple of args and kwargs to create a unique key.
            result = cache.get(key)
            if result == -1:  # Cache miss
                result = func(*args, **kwargs)
                cache.put(key, result)
            return result

        return wrapper

    return decorator
