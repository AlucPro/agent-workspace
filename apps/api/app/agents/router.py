from app.schemas.chat import ChatRequest, IntentType


class DecisionRouter:
    def route(self, request: ChatRequest, intent: IntentType) -> dict[str, bool]:
        return {
            "retrieval_needed": intent == IntentType.KNOWLEDGE_QA or request.use_knowledge_base,
            "tool_needed": intent == IntentType.TOOL_CALL,
        }


decision_router = DecisionRouter()
