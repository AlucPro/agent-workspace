from app.schemas.chat import ChatResponse, IntentType, SourceItem, ToolCallItem, TraceItem


class ResponseComposer:
    def compose(
        self,
        *,
        session_id: str,
        message_id: str,
        intent: IntentType,
        answer: str,
        sources: list[SourceItem],
        tool_calls: list[ToolCallItem],
        trace: list[TraceItem],
    ) -> ChatResponse:
        return ChatResponse(
            session_id=session_id,
            message_id=message_id,
            intent=intent,
            answer=answer,
            sources=sources,
            tool_calls=tool_calls,
            trace=trace,
        )


response_composer = ResponseComposer()
