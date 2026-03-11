import unittest
from unittest.mock import patch

from app.services.llm_service import llm_service


class LLMServiceTestCase(unittest.TestCase):
    @patch("app.services.llm_service.settings.openai_api_key", None)
    @patch("app.services.llm_service.settings.openai_model", None)
    def test_fallback_when_llm_config_missing(self) -> None:
        result = llm_service.generate_direct_answer("帮我整理这个需求")

        self.assertFalse(result.used_llm)
        self.assertIn("fallback", result.answer)
        self.assertEqual(result.trace_step, "llm_skipped: missing_openai_config")

    @patch("app.services.llm_service.settings.openai_api_key", "test-key")
    @patch("app.services.llm_service.settings.openai_model", "gpt-test")
    @patch.object(llm_service, "_call_chat_completions", return_value="这是 LLM 生成的 direct answer。")
    def test_returns_llm_answer_when_configured(self, mock_call) -> None:
        result = llm_service.generate_direct_answer("帮我整理这个需求")

        self.assertTrue(result.used_llm)
        self.assertEqual(result.answer, "这是 LLM 生成的 direct answer。")
        self.assertEqual(result.trace_step, "llm_response_generated: gpt-test")
        mock_call.assert_called_once_with("帮我整理这个需求")
