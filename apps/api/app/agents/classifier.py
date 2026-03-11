from app.schemas.chat import ChatRequest


class IntentClassifier:
    def classify(self, request: ChatRequest) -> str:
        message = request.message.lower()

        if request.use_knowledge_base:
            return "knowledge_qa"

        if any(keyword in message for keyword in ["增长率", "同比", "环比", "calculate", "计算", "%"]):
            return "tool_call"

        return "direct_answer"


intent_classifier = IntentClassifier()
