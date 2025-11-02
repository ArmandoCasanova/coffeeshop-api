import redis.asyncio as redis
from typing import Optional
import json
from app.core.settings import get_settings

settings = get_settings()


class RedisClient:
    _client: Optional[redis.Redis] = None

    @classmethod
    async def get_client(cls) -> redis.Redis:
        """Get or create Redis client"""
        if cls._client is None:
            cls._client = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return cls._client

    @classmethod
    async def close(cls):
        """Close Redis connection"""
        if cls._client:
            await cls._client.close()
            cls._client = None

    @classmethod
    async def get(cls, key: str) -> Optional[str]:
        """Get value from Redis"""
        client = await cls.get_client()
        return await client.get(key)

    @classmethod
    async def set(cls, key: str, value: str, ex: Optional[int] = None):
        """Set value in Redis with optional expiration"""
        client = await cls.get_client()
        await client.set(key, value, ex=ex)

    @classmethod
    async def delete(cls, key: str):
        """Delete key from Redis"""
        client = await cls.get_client()
        await client.delete(key)

    @classmethod
    async def get_json(cls, key: str) -> Optional[dict]:
        """Get JSON value from Redis"""
        value = await cls.get(key)
        return json.loads(value) if value else None

    @classmethod
    async def set_json(cls, key: str, value: dict, ex: Optional[int] = None):
        """Set JSON value in Redis with optional expiration"""
        await cls.set(key, json.dumps(value), ex=ex)
