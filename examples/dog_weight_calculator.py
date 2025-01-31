import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from agents.basic_agent import BasicAgent
from config.config import load_config
from tools.calculate import CalculateTool
from tools.base_tool import BaseTool


class AverageDogWeightTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="AverageDogWeightTool",
            description="Returns the average weight of a specific dog breed.",
            input_params={"name": "str"},
            output_format={"weight": "str"}
        )

    def execute(self, **kwargs):
        name = kwargs.get("name")
        if not isinstance(name, str):
            raise ValueError("The 'name' parameter must be a string representing the dog's breed.")
        
        # Mock data for demonstration purposes
        breed_weights = {
            "Scottish Terrier": "Scottish Terriers average 20 lbs",
            "Border Collie": "Border Collies average weight is 37 lbs",
            "Toy Poodle": "Toy Poodles average weight is 7 lbs"
        }
        
        return {"weight": breed_weights.get(name, "An average dog weighs 50 lbs")}


def main():
    # Load configuration
    config = load_config()
    
    # Initialize tools
    avg = AverageDogWeightTool()
    clc = CalculateTool()

    # Initialize agent with config
    abot = BasicAgent(
        tools=[avg, clc],
        config=config
    )

    print("Dog Weight Calculator Bot (type 'exit' to quit)")
    print("Example questions:")
    print("- How much does a Border Collie weigh?")
    print("- What is the combined weight of a Border Collie and a Scottish Terrier?")
    
    while True:
        question = input("\nYou: ")
        if question.lower() == 'exit':
            print("Goodbye!")
            for message in abot.messages:
                print(f"{message['role']}: {message['content']}")
            break
        response = abot(question)
        print(f"Bot: {response}")



if __name__ == "__main__":
    main() 