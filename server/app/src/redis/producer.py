from .config import RedisConnector


class Producer:
    def __init__(self, client):
        self.client = client

    # id=* means that the stream will make a new id for that particular element. We can also set our own id for the stream element
    async def add_to_stream(self, data: dict) -> bool:
        try:
            msg_id = await self.client.xadd(name="HUMAN_MESSAGES", id="*", fields=data)
            print(f"Message id {msg_id} added to HUMAN_MESSAGES stream")
            return msg_id

        except Exception as e:
            print(f"Error sending msg to stream => {e}")
