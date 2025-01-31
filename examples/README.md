# Framework Examples

This directory contains example implementations showing how to use and extend the agent framework.

## Simple Chat Example
`simple_chat.py` demonstrates basic usage with the built-in calculator tool:

```bash
python examples/simple_chat.py
```

### Dog Weight Calculator Example
`dog_weight_calculator.py` demonstrates combining multiple example tools to create a specialized agent that can:
- Get individual dog breed weights (using mock data)
- Calculate combined weights of multiple dogs

To run:

```bash
python examples/dog_weight_calculator.py
```

## Weather Agent Example
`weather_agent.py` shows how to:
- Create custom tools by extending BaseTool
- Combine multiple tools in one agent
- Handle complex queries requiring multiple tools
- Mock external API calls for development

To run:

```bash
python examples/weather_agent.py
```

## Creating Your Own Implementation

1. Create custom tools by extending BaseTool:

```python
class MyTool(BaseTool):
    def init(self):
        super().init(
            name="MyTool",
            description="What my tool does",
            input_params={"param1": "str"},
            output_format={"result": "str"}
        )

    def execute(self, kwargs):
        # Your tool logic here
        return {"result": "output"}
```

2. Initialize your agent with tools:
```python
agent = BasicAgent(
    tools=[MyTool()],
    config=load_config()
)
```

3. Use the agent in your application:

```python
response = agent("Your question here")
```

## Best Practices

1. Always provide clear tool descriptions
2. Handle errors gracefully in tool execution
3. Use type hints and documentation
4. Test your tools with various inputs
5. Consider rate limits for external APIs