from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.tool import ToolCallItem, ToolPlanItem


class IntentType(str, Enum):
    DIRECT_ANSWER = "direct_answer"
    KNOWLEDGE_QA = "knowledge_qa"
    TOOL_CALL = "tool_call"


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100, description="Conversation session identifier.")
    message: str = Field(min_length=1, max_length=4000, description="User message content.")
    use_knowledge_base: bool = Field(default=True, description="Whether retrieval is allowed for this request.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "session_1",
                "message": "帮我计算 2025 年同比增长率，去年收入 120 万，今年 156 万",
                "use_knowledge_base": False,
            }
        }
    }


class SourceItem(BaseModel):
    document_id: str = Field(min_length=1, description="Source document identifier.")
    file_name: str = Field(min_length=1, description="Original source file name.")
    chunk_id: str = Field(min_length=1, description="Retrieved chunk identifier.")
    content: str = Field(min_length=1, description="Retrieved chunk text.")


class TraceItem(BaseModel):
    step: str = Field(min_length=1, description="Short execution trace step.")


class AgentDecision(BaseModel):
    intent: IntentType
    reasoning_summary: str = Field(min_length=1, description="Compact reasoning summary safe for persistence.")
    retrieval_needed: bool = Field(description="Whether retrieval should run for this request.")
    tool_plan: list[ToolPlanItem] = Field(default_factory=list, description="Planned tool steps.")


class ChatResponse(BaseModel):
    session_id: str = Field(min_length=1, max_length=100, description="Conversation session identifier.")
    message_id: str = Field(min_length=1, max_length=100, description="Assistant message identifier.")
    intent: IntentType = Field(description="Intent chosen by the orchestrator.")
    answer: str = Field(min_length=1, description="Final assistant answer.")
    sources: list[SourceItem] = Field(default_factory=list, description="Retrieved supporting sources.")
    tool_calls: list[ToolCallItem] = Field(default_factory=list, description="Executed tool calls.")
    trace: list[TraceItem] = Field(default_factory=list, description="Execution trace steps.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "session_id": "session_1",
                "message_id": "msg_20260311130000000000",
                "intent": "tool_call",
                "answer": "这是工具调用路径的 mock 回答。任务：帮我计算 2025 年同比增长率，去年收入 120 万，今年 156 万。calculator_tool 返回结果：0.3",
                "sources": [],
                "tool_calls": [
                    {
                        "tool_name": "calculator_tool",
                        "tool_input": {"expression": "帮我计算 2025 年同比增长率，去年收入 120 万，今年 156 万"},
                        "tool_output": {"result": 0.3},
                    }
                ],
                "trace": [
                    {"step": "intent_detected: tool_call"},
                    {"step": "retrieval_needed: False"},
                    {"step": "tool_needed: True"},
                    {"step": "tool_executed: calculator_tool"},
                    {"step": "final_response_generated"},
                ],
            }
        }
    }
