import json
import logging
import re

from prompt_templates import (
    planner_template,
    executor_template,
    response_generator_template
)
from llm_providers.base_provider import BaseProvider
from llm_providers.openai_provider import OpenAIProvider
from utils.extract_xml import extract_xml
from utils.logging import setup_logging
from config.config import Config, load_config


class BasicAgent:
    def __init__(self, tools: list, config: Config = None):
        """
        Initialize the BasicAgent with tools and configuration.
        
        Args:
            tools (list): List of available tools
            config (Config, optional): Configuration object. If None, loads default config.
        """
        # Initialize configuration
        self.config = config or load_config()
        
        # Setup logging
        self.logger = setup_logging(self.config)
        
        # Initialize tools
        self.tools = {tool.name: tool for tool in tools}
        
        # Initialize LLM provider with config
        self.llm_provider = OpenAIProvider(
            api_key=self.config.llm.api_key,
            temperature=self.config.llm.temperature,
            max_tokens=self.config.llm.max_tokens
        )
        
        self.messages = []

        self.available_tools = self._get_tools_description()
        self.available_tools_with_params = self._get_tools_description(include_params=True)

        self.planner_prompt = planner_template.prompt
        self.executor_prompt = executor_template.prompt

        self.response_generator_prompt = response_generator_template.prompt.format(available_tools=self.available_tools)
        self.messages.append({"role": "system", "content": self.response_generator_prompt})

        self.action_re = re.compile(r'^Action: ({.*})$')
    
    def __call__(self, question):
        self.messages.append({"role": "user", "content": question})
        plan = self.planner(question)
        self.logger.debug(f"Plan: {plan}")
        if plan != "":
            try:
                answer_without_context = self.executor(plan, question)
            except Exception as e:
                self.logger.error(f"Failed to execute plan: {e}")
                answer_without_context = "I'm sorry, I couldn't find an answer to your question due to an internal error."
            self.messages.append({"role": "assistant", "content": f"<agent_answer>{answer_without_context}</agent_answer>"})
        answer = self.response_generator()
        self.messages.append({"role": "assistant", "content": answer})
        return answer
    
    def _get_tools_description(self, include_params: bool = False):
        """
        Returns a description of the available tools.
        """
        tools_description = []
        for tool in self.tools.values():
            tool_info = tool.info()
            params = ", ".join([f"{param} ({type_})" for param, type_ in tool_info["input_params"].items()])
            outputs = ", ".join([f"{field} ({type_})" for field, type_ in tool_info["output_format"].items()])
            tool_description = f"* {tool_info['name']}:\n  - Description: {tool_info['description']}"
            if include_params:
                tool_description += f"\n  - Parameters: {params if params else 'None'}"
                tool_description += f"\n  - Output Format: {outputs if outputs else 'None'}"
            tools_description.append(tool_description)
        return "\n\n".join(tools_description)

    def planner(self, question: str):
        """
        Generates a plan using the Planner module.
        """
        plan_prompt = self.planner_prompt.format(available_tools=self.available_tools, user_input=question)
        response = self.llm_provider.llm_call(plan_prompt, model=self.config.llm.model)
        plan = extract_xml(response, "plan")
        return plan.strip()

    def executor(self, plan: str, question: str, max_turns: int = 5):
        """
        Executes the given plan, handling Thought, Action, PAUSE, and Observation loops.
        """
        executor_messages = []
        system_prompt = self.executor_prompt.format(
            available_tools_with_params=self.available_tools_with_params
        )
        executor_messages.append({"role": "system", "content": system_prompt})
        
        next_prompt = f"Question: {question}\nPlan: {plan}"

        for _ in range(max_turns):
            self.logger.debug(f"Executing turn {_+1} of {max_turns}")
            executor_messages.append({"role": "user", "content": next_prompt})
            response = self.llm_provider.llm_call(
                messages=executor_messages,
                model=self.config.llm.model
            )
            executor_messages.append({"role": "assistant", "content": response})
            # Match JSON-like Action
            actions = [
                self.action_re.match(line.strip())
                for line in response.split('\n')
                if self.action_re.match(line.strip())
            ]
            self.logger.debug(f"Actions: {actions}")
            
            if actions:
                # Extract and parse the first action
                action_json = actions[0].group(1)
                try:
                    action_data = json.loads(action_json)
                    action = action_data.get("tool")
                    parameters = action_data.get("parameters", {})
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse action JSON: {action_json}. Error: {e}")
                    raise Exception(f"Failed to parse action JSON: {action_json}. Error: {e}")

                # Validate and execute the action
                if action not in self.tools:
                    self.logger.error(f"Unknown action: {action}")
                    raise Exception(f"Unknown action: {action}")

                self.logger.info(f"Running {action} with parameters {parameters}")

                observation = self.tools[action].execute(**parameters)
                self.logger.debug(f"Observation: {observation}")                
                
                # Update the prompt with the observation
                next_prompt = f"Observation: {json.dumps(observation)}"
            else:
                # If no action, the response might be the final answer
                self.logger.info("No more actions, returning final response")
                self.logger.debug(f"Executor messages: {executor_messages}")
                return response
        self.logger.debug(f"Executor messages: {executor_messages}")
        self.logger.error("Max turns reached without reaching an answer.")
        raise Exception("Max turns reached without reaching an answer.")

    
    def response_generator(self):
        """
        Generates a response to the user using a language model.
        """
        response = self.llm_provider.llm_call(messages=self.messages.copy(), model=self.config.llm.model)
        return response