import redis.asyncio as redis
import asyncio


async def main():
    # Подключение к Redis
    redis_client = redis.Redis(
        host='172.18.0.2',
        port=6388,
        password='passwd',
        decode_responses=True  # Для работы со строками
    )

    # Установка ключа
    key = "my_key"
    value = "my_value"
    await redis_client.set(key, value)
    print(f"Ключ '{key}' с значением '{value}' добавлен в Redis.")

    # Получение значения для проверки
    result = await redis_client.get(key)
    print(f"Значение ключа '{key}': {result}")

    # Закрытие соединения
    await redis_client.aclose()


# Запуск асинхронного метода
asyncio.run(main())
