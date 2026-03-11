import re
from dataclasses import dataclass

from app.schemas.chat import ChatRequest, IntentType


@dataclass(frozen=True)
class ClassificationResult:
    intent: IntentType
    reason: str


class IntentClassifier:
    tool_keywords = (
        "计算",
        "calculate",
        "calculator",
        "增长率",
        "同比",
        "环比",
        "百分比",
        "percentage",
        "求和",
        "sum",
        "平均",
        "average",
        "合计",
        "multiply",
        "除以",
    )
    knowledge_keywords = (
        "根据文档",
        "基于文档",
        "从文档里",
        "文档中",
        "知识库",
        "uploaded",
        "上传的",
        "这份prd",
        "这份prd",
        "这份jd",
        "岗位jd",
        "简历",
        "文件里",
        "材料里",
        "source",
    )
    arithmetic_pattern = re.compile(r"[\d\)\(]+\s*[\+\-\*/%]\s*[\d\(]")

    def classify(self, request: ChatRequest) -> IntentType:
        return self.classify_with_reason(request).intent

    def classify_with_reason(self, request: ChatRequest) -> ClassificationResult:
        normalized_message = self._normalize_message(request.message)

        if self._looks_like_tool_call(normalized_message):
            return ClassificationResult(
                intent=IntentType.TOOL_CALL,
                reason="用户请求包含明确计算或数值运算信号。",
            )

        if request.use_knowledge_base and self._looks_like_knowledge_qa(normalized_message):
            return ClassificationResult(
                intent=IntentType.KNOWLEDGE_QA,
                reason="用户开启知识库并且问题依赖文档内容。",
            )

        if request.use_knowledge_base and self._is_document_facing_question(normalized_message):
            return ClassificationResult(
                intent=IntentType.KNOWLEDGE_QA,
                reason="用户开启知识库，问题包含文档导向的问法。",
            )

        return ClassificationResult(
            intent=IntentType.DIRECT_ANSWER,
            reason="请求不依赖工具或外部文档，适合直接回答。",
        )

    @staticmethod
    def _normalize_message(message: str) -> str:
        return re.sub(r"\s+", " ", message.strip().lower())

    def _looks_like_tool_call(self, message: str) -> bool:
        return any(keyword in message for keyword in self.tool_keywords) or bool(self.arithmetic_pattern.search(message))

    def _looks_like_knowledge_qa(self, message: str) -> bool:
        return any(keyword in message for keyword in self.knowledge_keywords)

    @staticmethod
    def _is_document_facing_question(message: str) -> bool:
        return any(
            phrase in message
            for phrase in (
                "总结",
                "概括",
                "提炼",
                "风险点",
                "核心目标",
                "匹配度",
                "差距",
                "这份",
            )
        )


intent_classifier = IntentClassifier()
