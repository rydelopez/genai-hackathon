import os
import redis.asyncio as redis


class RedisConnector:
    def __init__(self):
        """Initialize settings for Redis server"""
        self.REDIS_URL = os.environ["REDIS_URL"]

    async def create_connection(self):
        """Makes an async connection"""
        self.connection = redis.from_url(self.REDIS_URL)

        return self.connection
