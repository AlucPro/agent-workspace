import unittest

from app.tools.calculator import calculator_tool


class CalculatorToolTestCase(unittest.TestCase):
    def test_growth_rate_request(self) -> None:
        result = calculator_tool.run(expression="帮我计算同比增长率，去年收入 120 万，今年 156 万")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["operation"], "growth_rate")
        self.assertEqual(result["result"], 0.3)
        self.assertEqual(result["formatted_result"], "30.00%")

    def test_arithmetic_expression_request(self) -> None:
        result = calculator_tool.run(expression="(156-120)/120")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["operation"], "arithmetic")
        self.assertEqual(result["result"], 0.3)

    def test_average_request(self) -> None:
        result = calculator_tool.run(expression="帮我计算 80 90 100 的平均值")

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["operation"], "average")
        self.assertEqual(result["result"], 90.0)

    def test_unsupported_expression(self) -> None:
        result = calculator_tool.run(expression="帮我预测明年的收入走势")

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["result"], "unsupported_expression")


if __name__ == "__main__":
    unittest.main()
