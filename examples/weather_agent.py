import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from tools.base_tool import BaseTool
from agents.basic_agent import BasicAgent
from config.config import load_config



class WeatherTool(BaseTool):
    def __init__(self, api_key):
        super().__init__(
            name="WeatherTool",
            description="Gets current weather for a given city",
            input_params={"city": "str"},
            output_format={"temperature": "float", "conditions": "str"}
        )
        self.api_key = api_key

    def execute(self, **kwargs):
        city = kwargs.get("city")
        if not city:
            raise ValueError("City parameter is required")

        # This is a mock implementation
        # In real usage, you would call an actual weather API
        weather_data = self._mock_weather_request(city)
        
        return {
            "temperature": weather_data["temp"],
            "conditions": weather_data["conditions"]
        }

    def _mock_weather_request(self, city):
        # Mock weather data for demonstration
        weather_data = {
            "New York": {"temp": 20.5, "conditions": "partly cloudy"},
            "London": {"temp": 15.0, "conditions": "rainy"},
            "Tokyo": {"temp": 25.0, "conditions": "sunny"},
        }
        return weather_data.get(city, {"temp": 18.0, "conditions": "unknown"})


class NewsSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="NewsSearchTool",
            description="Searches for recent news about a topic",
            input_params={"topic": "str"},
            output_format={"headlines": "list"}
        )

    def execute(self, **kwargs):
        topic = kwargs.get("topic")
        if not topic:
            raise ValueError("Topic parameter is required")

        # Mock news data
        return {
            "headlines": [
                f"Latest developments in {topic}",
                f"New research about {topic} revealed",
                f"Experts discuss {topic} implications"
            ]
        }


def main():
    # Load configuration
    config = load_config()
    
    # Initialize custom tools
    weather_tool = WeatherTool(api_key="demo_key")
    news_tool = NewsSearchTool()
    
    # Create agent with custom tools
    agent = BasicAgent(
        tools=[weather_tool, news_tool],
        config=config
    )
    
    print("Weather & News Assistant (type 'exit' to quit)")
    print("Example questions:")
    print("- What's the weather like in New York?")
    print("- Tell me the latest news about climate change")
    print("- How's the weather in London and what's the news about renewable energy?")
    
    while True:
        question = input("\nYou: ")
        if question.lower() == 'exit':
            break
            
        response = agent(question)
        print(f"Bot: {response}")


if __name__ == "__main__":
    main() 