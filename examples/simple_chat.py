import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from config.config import load_config
from tools.calculate import CalculateTool
from agents.basic_agent import BasicAgent


def main():
    # Load configuration
    config = load_config()
    
    # Initialize with just a calculator tool
    calculator = CalculateTool()
    
    # Create agent instance
    agent = BasicAgent(
        tools=[calculator],
        config=config
    )
    
    print("Math Assistant Bot (type 'exit' to quit)")
    print("Example questions:")
    print("- What is 15 * 45?")
    print("- Calculate the square root of 144")
    
    while True:
        question = input("\nYou: ")
        if question.lower() == 'exit':
            break
            
        response = agent(question)
        print(f"Bot: {response}")


if __name__ == "__main__":
    main() 