from tools.base_tool import BaseTool

class CalculateTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="CalculateTool",
            description="Performs mathematical calculations based on a given expression. The expression uses Python syntax.",
            input_params={"expression": "str"},
            output_format={"result": "float or int"}
        )

    def execute(self, **kwargs):
        expression = kwargs.get("expression", "")
        if not isinstance(expression, str):
            raise ValueError("The 'expression' parameter must be a string.")
        
        result = self._calculate(expression)
        
        return {"result": result}

    @staticmethod
    def _calculate(expression):
        """
        Safely evaluates a mathematical expression.
        Args:
            expression (str): The mathematical expression to evaluate.
        Returns:
            The result of the calculation.
        """
        try:
            return eval(expression)
        except Exception as e:
            raise ValueError(f"Invalid mathematical expression: {expression}. Error: {e}")