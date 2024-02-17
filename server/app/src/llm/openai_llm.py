import openai
from openai import ChatCompletion

from app.src.llm.base_llm import BaseLLM


class OpenAILLM(BaseLLM):
    """
    OpenAI LLM wrapper
    """

    def __init__(self, api_key, model_type, temperature, max_tokens):
        self.can_stream = True
        self.api_key = api_key
        self.model_type = model_type
        self.temperature = temperature
        self.max_tokens = max_tokens

        openai.api_key = api_key

    def format_input(
        self, user_input: str, history_list: list[dict[str, str]], context: str
    ) -> str:
        system_msg_formatted = [
            {
                "role": "system",
                "content": f"Here is the most relevant document to the user's request that was automatically retrieved: {context}",
            }
        ]

        history_formatted = [
            {"role": message["type"], "content": message["contents"]}
            for message in history_list
        ]

        new_message_formatted = [{"role": "user", "content": user_input}]

        return system_msg_formatted + history_formatted + new_message_formatted

    # Helper wrapper function to convert the openai generator
    async def token_generator(self, openai_generator):
        async for chunk in openai_generator:
            try:
                token = chunk["choices"][0]["delta"]["content"]
                yield token
            except KeyError:
                print("KeyError with chunk")
                return

    async def query(self, input_data: list[dict], stream=False):
        response = await ChatCompletion.acreate(
            model=self.model_type,
            messages=input_data,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stream=stream,
        )

        if stream:
            # Return an async generator with the tokens
            return self.token_generator(response)
        else:
            # Extract and return the assistant's reply
            assistant_reply = response["choices"][0]["message"]["content"]
            return assistant_reply

    def close(self):
        pass
