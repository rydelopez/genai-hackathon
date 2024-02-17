import json
import asyncio
from typing import Generator


class Consumer:
    def __init__(self, client):
        self.client = client

    async def get_message_stream(self, block: int, conversation_id: str) -> Generator:
        try:
            while True:
                response = await self.client.xread(
                    streams={f"CHATBOT_MESSAGES_{conversation_id}": "0-0"}, block=block
                )

                # If there is no response
                if len(response) == 0:
                    return

                # Retrieve entries from the stream
                stream_name, stream_entries = response[0]
                stream_name = stream_name.decode("utf-8")

                for message in stream_entries:
                    print(">>> message: ", message)

                    # Get the id and info for the message from the stream
                    message_id = message[0]
                    message_info = message[1]
                    message_type = message_info[b"type"].decode("utf-8")

                    # Delete message from CHATBOT_MESSAGES stream after it has been processed
                    await self.delete_message(
                        message_id=message_id.decode("utf-8"),
                        conversation_id=conversation_id,
                    )

                    if message_type == "streamed_response_stopper":
                        print(">>> received end of stream stop signal")
                        yield f"event: end-of-stream\ndata: none\n\n"
                        break
                    else:
                        yield f"data: {message_info[b'chunk'].decode('utf-8')}\n\n"
        except asyncio.CancelledError:
            pass

    async def consume_chatbot_message(
        self, block: int, conversation_id: str
    ) -> dict[str, str]:
        """
        Consumes messages from the stream of chatbot messages, and returns them.

        Returns:
            {message_type: message_text}
        """

        response = await self.client.xread(
            streams={f"CHATBOT_MESSAGES_{conversation_id}": "0-0"}, block=block
        )

        # If there is no response
        if len(response) == 0:
            return None

        # Retrieve entries from the stream
        stream_name, stream_entries = response[0]
        stream_name = stream_name.decode("utf-8")

        # Will remove this later, but just want to that only one stream (the CHATBOT_MESSAGES one)
        # is received
        assert len(response) == 1
        assert stream_name == f"CHATBOT_MESSAGES_{conversation_id}"

        # Process stream entries
        if len(stream_entries) == 0:
            return None

        # Extract the token and information from received message
        print(stream_entries, flush=True)
        # assert len(stream_entries) == 1

        # Return stream info
        return stream_entries

    async def delete_message(self, message_id, conversation_id: str):
        await self.client.xdel(f"CHATBOT_MESSAGES_{conversation_id}", message_id)
