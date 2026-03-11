import unittest

from app.agents.classifier import intent_classifier
from app.schemas.chat import ChatRequest, IntentType


class IntentClassifierTestCase(unittest.TestCase):
    def test_direct_answer_intent(self) -> None:
        request = ChatRequest(
            session_id="session_direct",
            message="帮我把这段需求整理成开发任务列表",
            use_knowledge_base=False,
        )

        result = intent_classifier.classify_with_reason(request)

        self.assertEqual(result.intent, IntentType.DIRECT_ANSWER)
        self.assertIn("直接回答", result.reason)

    def test_knowledge_qa_intent_with_document_signals(self) -> None:
        request = ChatRequest(
            session_id="session_kb",
            message="总结这份 PRD 里的核心目标，并列出风险点",
            use_knowledge_base=True,
        )

        result = intent_classifier.classify_with_reason(request)

        self.assertEqual(result.intent, IntentType.KNOWLEDGE_QA)
        self.assertIn("知识库", result.reason)

    def test_tool_call_intent_with_calculation_request(self) -> None:
        request = ChatRequest(
            session_id="session_tool",
            message="帮我计算 2025 年同比增长率，去年收入 120 万，今年 156 万",
            use_knowledge_base=False,
        )

        result = intent_classifier.classify_with_reason(request)

        self.assertEqual(result.intent, IntentType.TOOL_CALL)
        self.assertIn("计算", result.reason)

    def test_tool_call_has_priority_over_knowledge_flag(self) -> None:
        request = ChatRequest(
            session_id="session_priority",
            message="根据我上传的岗位 JD，帮我计算匹配率",
            use_knowledge_base=True,
        )

        result = intent_classifier.classify_with_reason(request)

        self.assertEqual(result.intent, IntentType.TOOL_CALL)


if __name__ == "__main__":
    unittest.main()
