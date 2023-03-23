import random
import redis
import pickle


OPENAI_TOKEN_LIST = [
	'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',
	'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',
	'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',
]

def get_token_openai():
    return random.choice(OPENAI_TOKEN_LIST)


class RedisDatabase():
    def __init__(self, host, port, timeout=60):
        self._redis = redis.Redis(host, port, socket_timeout=timeout)
    def get_value(self, key):
        result = self._redis.get(key)
        if result:
            return pickle.loads(result)
        else:
            return None

    def set_value(self, key, value, expire=None):
        self._redis.set(key, pickle.dumps(value), ex=expire)

