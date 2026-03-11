from app.agents.orchestrator import agent_orchestrator
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def handle_message(self, request: ChatRequest) -> ChatResponse:
        return agent_orchestrator.handle(request)


chat_service = ChatService()
