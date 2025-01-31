import pytest
from config.config import Config, LLMConfig

@pytest.fixture
def mock_config():
    return Config(
        llm=LLMConfig(
            provider="openai",
            model="gpt-4-turbo-preview",
            temperature=0.1,
            max_tokens=4096,
            api_key="test-key"
        ),
        debug=True,
        log_level="DEBUG"
    ) 