from app.agents.classifier import intent_classifier
from app.agents.composer import response_composer
from app.agents.router import decision_router
from app.schemas.chat import AgentDecision, ChatRequest, ChatResponse, IntentType, SourceItem, ToolCallItem, TraceItem
from app.tools.calculator import calculator_tool
from app.tools.document_lookup import document_lookup_tool
from app.utils.ids import generate_message_id


class AgentOrchestrator:
    def handle(self, request: ChatRequest) -> ChatResponse:
        classification = intent_classifier.classify_with_reason(request)
        intent = classification.intent
        route = decision_router.route(request, intent)
        trace = [
            TraceItem(step=f"intent_detected: {intent}"),
            TraceItem(step=f"retrieval_needed: {route['retrieval_needed']}"),
            TraceItem(step=f"tool_needed: {route['tool_needed']}"),
        ]

        decision = AgentDecision(
            intent=intent,
            reasoning_summary=classification.reason,
            retrieval_needed=route["retrieval_needed"],
            tool_plan=[],
        )

        sources: list[SourceItem] = []
        tool_calls: list[ToolCallItem] = []

        if decision.retrieval_needed:
            lookup_result = document_lookup_tool.run(query=request.message, top_k=3)
            sources = lookup_result["matched_chunks"]
            trace.append(TraceItem(step=f"retrieval_performed: {len(sources)} chunks"))

        if route["tool_needed"]:
            tool_result = calculator_tool.run(expression=request.message)
            tool_calls.append(
                ToolCallItem(
                    tool_name=calculator_tool.name,
                    tool_input={"expression": request.message},
                    tool_output={"result": tool_result["result"]},
                )
            )
            trace.append(TraceItem(step="tool_executed: calculator_tool"))

        answer = self._build_answer(intent=intent, request=request, sources=sources, tool_calls=tool_calls)
        trace.append(TraceItem(step="final_response_generated"))

        return response_composer.compose(
            session_id=request.session_id,
            message_id=generate_message_id(),
            intent=intent,
            answer=answer,
            sources=sources,
            tool_calls=tool_calls,
            trace=trace,
        )

    @staticmethod
    def _build_answer(
        *,
        intent: IntentType,
        request: ChatRequest,
        sources: list[SourceItem],
        tool_calls: list[ToolCallItem],
    ) -> str:
        if intent == IntentType.KNOWLEDGE_QA:
            source_summary = "；".join(source.content for source in sources[:2]) or "当前知识库暂无匹配内容。"
            return f"这是基于知识库的 mock 回答。你问的是：{request.message}。命中的关键信息：{source_summary}"

        if intent == IntentType.TOOL_CALL and tool_calls:
            result = tool_calls[0].tool_output["result"]
            return f"这是工具调用路径的 mock 回答。任务：{request.message}。calculator_tool 返回结果：{result}"

        return f"这是 direct_answer 路径的 mock 回答。任务：{request.message}"


agent_orchestrator = AgentOrchestrator()
