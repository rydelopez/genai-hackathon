# This is the base LLM class that all other LLM wrappers should be extended from
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def __init__(self):
        """
        Initializes an LLM wrapper with the necessary information for connecting
        to and using the endpoint. Depending on the LLM provider, we may or may
        not need a URL pertaining to the endpoint.
        """
        self.endpoint_url: str
        self.model_name: str
        self.headers = None
        self.payload = None
        self.can_stream = False

        # We should also set any relevant API keys here, or other config variables.

    @abstractmethod
    def format_input(self, user_input: str, history=None) -> str:
        """
        Converts the user input, message history, and external information in an appropriate
        manner to be fed into the model with the `query` method. This will typically be a string,
        but may be of another form depending on the provider (e.g. OpenAI)
        """
        return user_input

    @abstractmethod
    async def query(self, input: str, stream=False):
        """
        Queries the LLM and returns a response. The response will be a string output
        if stream=False, or an async generator if stream=True.

        Args:
            input (str): The input string to be queried.
            stream (bool): If True, the response will be returned as an async generator that yields tokens.
                        If False, the response will be a single string output.

        Returns:
            Union[str, AsyncGenerator[str, None]]: The response from the LLM. A string if stream=False,
                                                or an async generator yielding tokens if stream=True.
        """
        pass

    @abstractmethod
    def close(self):
        """
        This method should be used to close any possible connections, or reset any configuration
        variables (e.g. API keys) to their default/null values.
        """
        pass
