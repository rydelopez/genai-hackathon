
from fastapi import (
    APIRouter,
)

from app.src.redis.config import RedisConnector
from app.src.schema.conversation import Message
from app.src.vdb.weaviate_connector import WeaviateVDB
from app.src.redis.history import ConversationHistory

router = APIRouter()
redis_connector = RedisConnector()
weaviate_connector = WeaviateVDB()

from app.src.llm.openai_llm import OpenAILLM


#function for handling chat input
@router.post("/chatbot")
async def chatbot(
    client_message: Message
):

    #async connection to the redis server
    redis_client = await redis_connector.create_connection()

    #ConversationHistory setup
    history = ConversationHistory(redis_client)

    # Instantiate the LLM instance
    # - Moving this outside the loop for now, but when we deal with API tokens
    #   we may have to figure out a way to safely handle state changes
    llm = OpenAILLM("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", "gpt-3.5-turbo", 1, 100)

    # Read from the stream (message from the user)
    user_message = client_message.message
    conversation_id = client_message.conversation_id

    # Retrieve the appropriate data from the vector database based off of the user's question
    retrieved_doc = weaviate_connector.query_documents(
        user_message, lesson_id=client_message.lesson_id
    )

    # Get the old chat history
    history_dict = await history.get_history(conversation_id)

    # Format the input for the LLM wrapper
    llm_input = llm.format_input(
        user_input=user_message, history_list=history_dict, context=retrieved_doc
    )

    # When we query with stream=False, we will just get a string
    llm_response = await llm.query(llm_input, True)

    # Update chat history with new user + bot response
    await history.append_message(conversation_id, "user", user_message)
    await history.append_message(conversation_id, "chatbot", llm_response)