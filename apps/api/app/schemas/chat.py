from pydantic import BaseModel, Field

from app.schemas.tool import ToolCallItem, ToolPlanItem


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1, max_length=4000)
    use_knowledge_base: bool = True


class SourceItem(BaseModel):
    document_id: str
    file_name: str
    chunk_id: str
    content: str


class TraceItem(BaseModel):
    step: str


class AgentDecision(BaseModel):
    intent: str
    reasoning_summary: str
    retrieval_needed: bool
    tool_plan: list[ToolPlanItem] = Field(default_factory=list)


class ChatResponse(BaseModel):
    session_id: str
    message_id: str
    intent: str
    answer: str
    sources: list[SourceItem] = Field(default_factory=list)
    tool_calls: list[ToolCallItem] = Field(default_factory=list)
    trace: list[TraceItem] = Field(default_factory=list)
