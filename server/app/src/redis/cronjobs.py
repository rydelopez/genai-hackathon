
from app.src.redis.config import RedisConnector
from datetime import datetime
redis_connector = RedisConnector()

MINUTES_BUFFER = 10
EXPIRED_BUFFER = MINUTES_BUFFER * 60000

async def scrape_old_conversations():
    redis_client = await redis_connector.create_connection()
    # might need to change this if we implement a cache layer
    keys = [key.decode("utf-8") for key in redis_client.scan_iter(match="*", count=10000)]
    current_time = datetime.now()

    for key in keys:
        value = await redis_client.get(key)
        if value["last_updated"] + EXPIRED_BUFFER < current_time:
            value["last_updated"] = None
            value["conversation_started"] = None
        

