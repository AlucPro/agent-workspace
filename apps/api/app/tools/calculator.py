import re
from typing import Dict, Union

from app.tools.base import Tool


class CalculatorTool(Tool):
    name = "calculator_tool"
    description = "Safely evaluates simple arithmetic expressions."

    _allowed_pattern = re.compile(r"^[0-9\.\+\-\*\/\(\)\s%]+$")
    _number_pattern = re.compile(r"\d+(?:\.\d+)?")

    def run(self, **kwargs: str) -> Dict[str, Union[float, str]]:
        expression = kwargs["expression"]

        if any(keyword in expression for keyword in ["同比", "增长率", "环比"]):
            parsed = self._parse_growth_rate(expression)
            if parsed is not None:
                return {"result": round(parsed, 4)}

        sanitized = expression.replace("去年收入", "").replace("今年", "").replace("收入", "")

        if not self._allowed_pattern.match(sanitized):
            return {"result": "unsupported_expression"}

        normalized = sanitized.replace("%", "/100")
        try:
            result = eval(normalized, {"__builtins__": {}}, {})
        except Exception:
            return {"result": "calculation_failed"}

        return {"result": round(float(result), 4)}

    def _parse_growth_rate(self, expression: str) -> Union[float, None]:
        values = [float(value) for value in self._number_pattern.findall(expression)]
        if len(values) < 2 or values[-2] == 0:
            return None
        previous, current = values[-2], values[-1]
        return (current - previous) / previous


calculator_tool = CalculatorTool()
