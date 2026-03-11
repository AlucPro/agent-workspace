import ast
import re
from typing import Dict, List, Optional, Union

from app.tools.base import Tool


class CalculatorTool(Tool):
    name = "calculator_tool"
    description = "Safely evaluates simple arithmetic expressions."

    _number_pattern = re.compile(r"\d+(?:\.\d+)?")
    _expression_pattern = re.compile(r"[\d\.\+\-\*\/%\(\)\s]+")

    def run(self, **kwargs: str) -> Dict[str, Union[float, str]]:
        expression = kwargs["expression"]

        if any(keyword in expression for keyword in ["同比", "增长率", "环比"]):
            parsed = self._parse_growth_rate(expression)
            if parsed is not None:
                previous, current = parsed
                result = (current - previous) / previous
                return self._success_response(
                    operation="growth_rate",
                    result=result,
                    expression=f"({current}-{previous})/{previous}",
                    explanation="按(本期-上期)/上期计算。",
                    formatted_result=f"{result * 100:.2f}%",
                )

        if any(keyword in expression for keyword in ["平均", "average"]):
            values = self._extract_numbers(expression)
            if values:
                result = sum(values) / len(values)
                return self._success_response(
                    operation="average",
                    result=result,
                    expression="average(" + ", ".join(self._format_number(value) for value in values) + ")",
                    explanation="对识别到的数字求平均值。",
                )

        if any(keyword in expression for keyword in ["求和", "总和", "合计", "sum"]):
            values = self._extract_numbers(expression)
            if values:
                result = sum(values)
                return self._success_response(
                    operation="sum",
                    result=result,
                    expression=" + ".join(self._format_number(value) for value in values),
                    explanation="对识别到的数字求和。",
                )

        normalized_expression = self._normalize_expression(expression)
        if not normalized_expression:
            return self._error_response("unsupported_expression")

        try:
            result = self._safe_eval(normalized_expression)
        except Exception:
            return self._error_response("calculation_failed", normalized_expression)

        return self._success_response(
            operation="arithmetic",
            result=result,
            expression=normalized_expression,
            explanation="按标准算术表达式计算。",
        )

    def _parse_growth_rate(self, expression: str) -> Optional[tuple[float, float]]:
        values = self._extract_numbers(expression)
        if len(values) < 2 or values[-2] == 0:
            return None
        return values[-2], values[-1]

    def _extract_numbers(self, expression: str) -> List[float]:
        return [float(value) for value in self._number_pattern.findall(expression)]

    def _normalize_expression(self, expression: str) -> str:
        normalized = expression.lower()
        replacements = {
            "乘以": "*",
            "x": "*",
            "×": "*",
            "除以": "/",
            "加上": "+",
            "减去": "-",
            "（": "(",
            "）": ")",
            " ": "",
        }
        for source, target in replacements.items():
            normalized = normalized.replace(source, target)

        matches = self._expression_pattern.findall(normalized)
        candidate = "".join(matches).strip()
        if not candidate:
            return ""

        return candidate.replace("%", "/100")

    def _safe_eval(self, expression: str) -> float:
        node = ast.parse(expression, mode="eval")
        return float(self._eval_node(node.body))

    def _eval_node(self, node: ast.AST) -> float:
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Mod):
                return left % right
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            operand = self._eval_node(node.operand)
            return operand if isinstance(node.op, ast.UAdd) else -operand
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)

        raise ValueError("Unsupported expression")

    def _success_response(
        self,
        *,
        operation: str,
        result: float,
        expression: str,
        explanation: str,
        formatted_result: Optional[str] = None,
    ) -> Dict[str, Union[float, str]]:
        rounded = round(float(result), 4)
        return {
            "status": "success",
            "operation": operation,
            "expression": expression,
            "result": rounded,
            "formatted_result": formatted_result or self._format_number(rounded),
            "explanation": explanation,
        }

    def _error_response(self, error: str, expression: str = "") -> Dict[str, Union[float, str]]:
        return {
            "status": "error",
            "operation": "arithmetic",
            "expression": expression,
            "result": error,
            "formatted_result": error,
            "explanation": "无法从输入中提取可执行的安全算式。",
        }

    @staticmethod
    def _format_number(value: float) -> str:
        if value.is_integer():
            return str(int(value))
        return f"{value:.4f}".rstrip("0").rstrip(".")


calculator_tool = CalculatorTool()
