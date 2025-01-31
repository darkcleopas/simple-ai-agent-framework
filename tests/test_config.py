import os
import pytest
from config.config import Config, load_config

def test_config_from_yaml(tmp_path):
    config_content = """
    llm:
        provider: openai
        model: test-model
        temperature: 0.5
    debug: true
    log_level: DEBUG
    """
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(config_content)
    
    config = Config.from_yaml(str(config_file))
    assert config.llm.model == "test-model"
    assert config.llm.temperature == 0.5
    assert config.debug is True

def test_config_from_env():
    os.environ["OPENAI_API_KEY"] = "test-key"
    os.environ["LLM_MODEL"] = "env-model"
    os.environ["DEBUG"] = "true"
    
    config = Config()
    config.update_from_env()
    
    assert config.llm.api_key == "test-key"
    assert config.llm.model == "env-model"
    assert config.debug is True 