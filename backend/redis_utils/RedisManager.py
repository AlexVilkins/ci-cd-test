import pickle

import redis.asyncio as redis


class RedisManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='redis',
            port=6388,
            password='passwd',
            decode_responses=False
        )

    async def add_value(self, key, value):
        serialized_value = pickle.dumps(value)
        await self.redis_client.set(key, serialized_value)
        print(f"Ключ '{key}' с значением '{value}' добавлен в Redis.")
        await self.redis_client.publish(key, serialized_value)

    async def get_value(self, key):
        result = await self.redis_client.get(key)
        return pickle.loads(result)


redis_connection = RedisManager()
