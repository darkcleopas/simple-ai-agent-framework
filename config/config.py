from dataclasses import dataclass, field
from typing import Optional
import os
import yaml



@dataclass
class LLMConfig:
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    temperature: float = 0.1
    max_tokens: int = 4096
    api_key: Optional[str] = None


@dataclass
class Config:
    llm: LLMConfig = field(default_factory=LLMConfig)
    debug: bool = False
    log_level: str = "INFO"

    @classmethod
    def from_yaml(cls, file_path: str) -> 'Config':
        if not os.path.exists(file_path):
            return cls()
        
        with open(file_path, 'r') as f:
            config_dict = yaml.safe_load(f)
            
        llm_config = LLMConfig(**config_dict.get('llm', {}))
        return cls(
            llm=llm_config,
            debug=config_dict.get('debug', False),
            log_level=config_dict.get('log_level', "INFO")
        )

    def update_from_env(self):
        """Update config from environment variables"""
        if os.getenv("OPENAI_API_KEY"):
            self.llm.api_key = os.getenv("OPENAI_API_KEY")
        
        if os.getenv("LLM_MODEL"):
            self.llm.model = os.getenv("LLM_MODEL")
            
        if os.getenv("DEBUG"):
            self.debug = os.getenv("DEBUG").lower() == "true"
            
        if os.getenv("LOG_LEVEL"):
            self.log_level = os.getenv("LOG_LEVEL")


def load_config(config_path: Optional[str] = None) -> Config:
    """Load configuration from file and environment variables"""
    if config_path is None:
        config_path = os.getenv("CONFIG_PATH", "config.yaml")
    
    config = Config.from_yaml(config_path)
    config.update_from_env()
    return config 