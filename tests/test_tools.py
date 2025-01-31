import pytest
from tools.calculate import CalculateTool


class TestCalculateTool:
    @pytest.fixture
    def calculator(self):
        return CalculateTool()

    def test_basic_arithmetic(self, calculator):
        """Test basic arithmetic operations"""
        # Addition
        assert calculator.execute(expression="2 + 2")["result"] == 4
        # Subtraction
        assert calculator.execute(expression="5 - 3")["result"] == 2
        # Multiplication
        assert calculator.execute(expression="4 * 3")["result"] == 12
        # Division
        assert calculator.execute(expression="10 / 2")["result"] == 5

    def test_complex_expressions(self, calculator):
        """Test more complex mathematical expressions"""
        # Multiple operations
        assert calculator.execute(expression="2 + 3 * 4")["result"] == 14
        # Parentheses
        assert calculator.execute(expression="(2 + 3) * 4")["result"] == 20
        # Float results
        assert calculator.execute(expression="10 / 3")["result"] == pytest.approx(3.333333, rel=1e-5)
        # Powers
        assert calculator.execute(expression="2 ** 3")["result"] == 8

    def test_error_handling(self, calculator):
        """Test error handling for invalid inputs"""
        # Invalid expression
        with pytest.raises(ValueError):
            calculator.execute(expression="2 + * 3")
        
        # Division by zero
        with pytest.raises(ValueError):
            calculator.execute(expression="1/0")
        
        # Invalid type
        with pytest.raises(ValueError):
            calculator.execute(expression=123)  # Should be string
        
        # Empty expression
        with pytest.raises(ValueError):
            calculator.execute(expression="")

    def test_output_format(self, calculator):
        """Test that the output follows the expected format"""
        result = calculator.execute(expression="2 + 2")
        assert isinstance(result, dict)
        assert "result" in result
        assert isinstance(result["result"], (int, float)) 