# JSON caching methods
import os
import json
from datetime import datetime

from celery import Celery
REDIS_URL = os.environ.get("REDIS_URL")

celery_app = Celery("main_celery_app", broker=REDIS_URL)

# Redis Schema
# Type 1: Current Conversation
# Key: conversation:{parent_id}
# Value: []

# Key: metadata:{parent_id}
# Value: {num_questions: int, unique_words: set, total_response_time: int, start_time: datetime, last_time: datetime}

# Key: wordset:{parent_id}
# Value: wordset

class ConversationHistory:
    ALLOWED_MESSAGE_TYPES = ["user", "assistant", "system"]
    DUMMY_VALUE = "dummy"
    EXPIRED_BUFFER = 10 * 60000

    def __init__(self, redis_client):
        """Initialize our conversation history with a Redis cache"""
        self.client = redis_client

    async def append_message(self, parent_id, message_type, message_contents, response_time=0):
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
        # assuming these structures have formats of key "conversation:{parent_id}"
        redis_key = f"conversation:{parent_id}"
        await self.client.rpush(redis_key, message_json)
        await self.update_metadata(parent_id, message_type, message_contents, response_time)
        return {
            "msg": f"Message {message_contents} of type {message_type} appended to conversation {parent_id}."
        }

    async def update_metadata(self, parent_id, message_type, message_contents, response_time):
        metadata_key = f"metadata:{parent_id}"
        wordset_key = f"wordset:{parent_id}"
        stopwords_key = f"stopwords"
        time = datetime.now()
        metadata = await self.client.get(metadata_key)

        if message_type == "user":
            metadata["num_questions"] += 1
            metadata["num_sentences"] += len(message_contents.split(".")) - 1
            metadata["total_response_time"] += response_time
            cleaned_words = []
            for word in message_contents:
                if not self.client.sismember(stopwords_key, word):
                    cleaned_words.append(word)
            self.client.sadd(wordset_key, cleaned_words)
        
        if metadata["start_time"] is None:
            metadata["start_time"] = time
        metadata["last_time"] = time

        await self.redis_client.put(metadata_key, metadata)
    
    # have a function that goes through all of the keys and EXPIRES old messages
    
    async def process_expired_conversations(self):
        keys = [key.decode("utf-8") for key in self.redis_client.scan_iter(match="metadata:*", count=10000)]
        current_time = datetime.now()
        for key in keys:
            value = await self.redis_client.get(key)
            if value["last_updated"] + self.EXPIRED_BUFFER < current_time:
                parent_id = key.split(":")[1]
                self.update_db(parent_id)
                self.reset_conversation(parent_id)
    
    async def make_question_answers_answers(conversation):
        question_answers = []
        type = "non-user"
        curr = {}

        for obj in conversation:
            if obj["type"] == "user" and type == "user":
                curr["answer"] += " " + obj["contents"]
            elif obj["type"] != "user" and type == "user":
                question_answers.append(curr)
                type = "non-user"
                curr = {}
            elif obj["type"] == "user" and type != "user":
                type = "user"
                curr["question"] = obj["contents"]
            else:
                curr["question"] += " " + obj["contents"]
        
        question_answers.append(curr)
        return question_answers[1:]

    async def update_db(self, parent_id):
        metadata_key = f"metadata:{parent_id}"
        wordset_key = f"wordset:{parent_id}"
        metadata = await self.redis_client.get(metadata_key)
        metadata["num_unique_words"] = await self.redis_client.scard(wordset_key)
        conversation_key = f"conversation:{parent_id}"
        conversation = await self.redis_client.get(conversation_key)

        questions_answers = self.make_question_answers(conversation)
        answers = [obj["answer"] for obj in questions_answers]

        conversation_id = celery_app.send_task("app.src.celery.tasks.add_conversation_metadata", args=[parent_id, metadata], queue="celery")
        celery_app.send_task("app.src.celery.tasks.calculate_nlp_metrics", args=[conversation_id, answers], queue="celery")
        celery_app.send_task("app.src.celery.tasks.add_conversation_to_db", args=[conversation_id, questions_answers], queue="celery")
    
    async def reset_conversation(self, parent_id):
        # reset conversation
        conversation_key = f"conversation:{parent_id}"
        await self.redis_client.lpush(conversation_key, self.DUMMY_VALUE)
        await self.redis_client.ltrim(conversation_key, 1, 0)

        # reset metadata
        metadata_key = f"metadata:{parent_id}"
        await self.redis_client.set(metadata_key, {
            "num_questions": 0,
            "num_sentences": 0,
            "total_response_time": 0,
            "start_time": None,
            "last_time": None
        })

        # reset wordset
        wordset_key = f"wordset:{parent_id}"
        await self.redis_client.delete(wordset_key)
        await self.redis_client.sadd(wordset_key, self.DUMMY_VALUE)
        await self.redis_client.srem(wordset_key, self.DUMMY_VALUE)

    async def get_history(self, parent_id) -> list[dict[str, str]]:
        """
        Retrieves chat history for this conversation from Redis

        converation_id: string
        """

        redis_key = f"conversation:{parent_id}"

        # Get list of json items
        json_list = await self.client.lrange(redis_key, 0, -1)

        # Parse
        return [json.loads(message_str) for message_str in json_list]