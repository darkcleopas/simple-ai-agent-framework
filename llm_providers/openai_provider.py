from dotenv import load_dotenv
from openai import OpenAI
import os

from llm_providers.base_provider import BaseProvider


class OpenAIProvider(BaseProvider):
    def __init__(
        self,
        api_key: str = None,
        temperature: float = 0.1,
        max_tokens: int = 4096
    ):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key (str, optional): OpenAI API key.
            temperature (float, optional): Sampling temperature.
            max_tokens (int, optional): Maximum tokens for response.
        """
        super().__init__(api_key, temperature, max_tokens)
        self.client = OpenAI(api_key=self.api_key)

    def llm_call(
        self,
        prompt: str = None,
        system_prompt: str = None,
        model: str = "gpt-4o-mini",
        messages: list = [],
        max_tokens: int = None,
        temperature: float = None,
    ) -> str:
        """
        Call OpenAI API.
        """
        # Use instance defaults if not provided
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        temperature = temperature if temperature is not None else self.temperature

        if messages:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            if system_prompt:
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ]
            else:
                messages = [{"role": "user", "content": prompt}]

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        return response.choices[0].message.content
