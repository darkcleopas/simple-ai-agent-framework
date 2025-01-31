from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """
    Abstract base class for providers interacting with LLMs.
    """
    def __init__(
        self,
        api_key: str = None,
        temperature: float = 0.1,
        max_tokens: int = 4096
    ):
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def llm_call(
        self,
        prompt: str = None,
        system_prompt: str = None,
        model: str = None,
        messages: list = [],
        max_tokens: int = None,
        temperature: float = None,
    ) -> str:
        """
        Abstract method to call the LLM. Must be implemented by subclasses.

        Args:
            prompt (str): The user prompt to send to the model.
            system_prompt (str, optional): The system prompt to send to the model.
            model (str, optional): The model to use for the call.
            messages (list, optional): A list of messages for context.
            max_tokens (int, optional): The maximum number of tokens for the response.
            temperature (float, optional): The sampling temperature for response diversity.

        Returns:
            str: The content of the response from the language model.
        """
        pass
