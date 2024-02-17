# JSON caching methods
import json


class ConversationHistory:
    ALLOWED_MESSAGE_TYPES = ["user", "assistant", "system"]

    def __init__(self, redis_client):
        """Initialize our conversation history with a Redis cache"""
        self.client = redis_client

    async def append_message(self, conversation_id, message_type, message_contents):
        """
        Appends a message to a list of back-and-forth messages in a conversation

        converation_id: string
        message_type: "user" | "assistant" | "system"
        message_contents: string

        """
        if message_type not in self.ALLOWED_MESSAGE_TYPES:
            raise ValueError(
                "Invalid message type. Allowed types are 'user', 'assistant', or 'system'."
            )

        message = {"type": message_type, "contents": message_contents}
        message_json = json.dumps(message)

        # assuming this conversation history is a redis list
        # assuming these structures have formats of key "conversation:{conversation_id}"
        redis_key = f"conversation:{conversation_id}"
        await self.client.rpush(redis_key, message_json)
        return {
            "msg": f"Message {message_contents} of type {message_type} appended to conversation {conversation_id}"
        }

    async def get_history(self, conversation_id) -> list[dict[str, str]]:
        """
        Retrieves chat history for this conversation from Redis

        converation_id: string
        """

        redis_key = f"conversation:{conversation_id}"

        # Get list of json items
        json_list = await self.client.lrange(redis_key, 0, -1)

        # Parse
        return [json.loads(message_str) for message_str in json_list]
