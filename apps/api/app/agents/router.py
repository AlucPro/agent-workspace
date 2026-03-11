from app.schemas.chat import ChatRequest


class DecisionRouter:
    def route(self, request: ChatRequest, intent: str) -> dict[str, bool]:
        return {
            "retrieval_needed": intent == "knowledge_qa" or request.use_knowledge_base,
            "tool_needed": intent == "tool_call",
        }


decision_router = DecisionRouter()
