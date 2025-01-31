# Simple AI Agent Framework

A lightweight, framework-independent implementation of AI agents based on the ReAct (Reasoning and Acting) paradigm. This project aims to provide a simple and reliable quick start for building AI agents without the complexity of larger frameworks.

## Overview

The project implements a basic agent architecture that can:
- Process user queries through a structured planning and execution pipeline
- Use various tools to gather and process information
- Generate coherent responses based on tool outputs
- Handle errors gracefully
- Support multiple LLM providers (currently OpenAI)

## Current Implementation

### Core Components

1. **Basic Agent**
   - ReAct-based implementation (Reasoning and Acting)
   - Three-step process: Planning, Execution, Response Generation
   - Support for multiple tools
   - Conversation history management

2. **LLM Providers**
   - Abstract base provider interface
   - OpenAI implementation
   - Extensible for other providers

3. **Tools System**
   - Base tool class with standardized interface
   - Implemented tools:
     - AverageDogWeightTool (example tool)
     - CalculateTool (mathematical operations)

4. **Prompt Templates**
   - Structured prompts for:
     - Planning
     - Execution
     - Response generation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Basic usage example:

```python
from agents.basic_agent import BasicAgent
from config.config import load_config
from tools.calculate import CalculateTool

# Load configuration
config = load_config()

# Initialize tools
calc_tool = CalculateTool()

# Create agent
agent = BasicAgent(
    tools=[calc_tool],
    config=config
)

# Ask a question
response = agent("What is 15 * 45?")
print(response)
```

## Testing

### Overview
The project uses pytest as the primary testing framework. Tests are organized by component type and focus on ensuring the reliability of core functionalities.

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools.py

# Run with coverage report
pytest --cov=./ --cov-report=term-missing
```

### Test Structure

1. **Unit Tests**
   - Tools: Test individual tool functionality and error handling
   <!-- - Providers: Test LLM provider implementations -->
   - Config: Test configuration loading and validation
   - Prompt Templates: Test template rendering and validation
   <!-- - Utils: Test helper functions and utilities -->


### Writing Tests

Example of a tool test:
```python
def test_tool_functionality():
    tool = SomeTool()
    result = tool.execute(input_param="test")
    assert "expected_key" in result
    assert result["expected_key"] == "expected_value"
```

## TODO List

### Completed ✅
- [x] Basic agent implementation with ReAct framework
- [x] Tool system architecture
- [x] Base provider interface for LLMs
- [x] OpenAI provider implementation
- [x] Prompt templates structure
- [x] Basic error handling
- [x] Conversation history management
- [x] Example tools implementation
- [x] XML response parsing utility
- [x] Config file support
- [x] Environment variables handling
- [x] Unit tests
- [x] Usage examples
- [x] Installation guide

### Pending 🚀
- [ ] Testing
  - [ ] Integration tests
  - [ ] Prompt testing framework
- [ ] Features
  - [ ] Memory system
  - [ ] Async support
  - [ ] Streaming responses
  - [ ] Tool validation system
  - [ ] Cost tracking
<!-- - [ ] Monitoring
  - [ ] Performance metrics
  - [ ] Usage statistics
  - [ ] Error tracking -->
- [ ] Documentation
  - [ ] API documentation
  - [ ] Tool creation guide
- [ ] Tools
  - [ ] Web search
  - [ ] Data retrieval
  - [ ] File operations

## Contributing

This project is under development. Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
'''
