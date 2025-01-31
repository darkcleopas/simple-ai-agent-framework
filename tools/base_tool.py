from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Base class for all tools in the system.
    """
    def __init__(self, name: str, description: str, input_params: dict, output_format: dict):
        """
        Initializes the tool with its properties.

        :param name: Name of the tool.
        :param description: Description of the tool's functionality.
        :param input_params: Expected input parameters (format: {"param": "type"}).
        :param output_format: Expected output format (format: {"field": "type"}).
        """
        self.name = name
        self.description = description
        self.input_params = input_params
        self.output_format = output_format

    @abstractmethod
    def execute(self, **kwargs):
        """
        Abstract method to execute the tool.
        Each tool must implement its logic here.

        :param kwargs: Arguments corresponding to the input parameters.
        :return: Output matching the output_format.
        """
        pass

    def info(self):
        """
        Returns information about the tool.
        """
        return {
            "name": self.name,
            "description": self.description,
            "input_params": self.input_params,
            "output_format": self.output_format
        }