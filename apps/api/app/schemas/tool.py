from typing import Any

from pydantic import BaseModel, Field


class ToolPlanItem(BaseModel):
    tool_name: str
    args: dict[str, Any] = Field(default_factory=dict)


class ToolCallItem(BaseModel):
    tool_name: str
    tool_input: dict[str, Any] = Field(default_factory=dict)
    tool_output: dict[str, Any] = Field(default_factory=dict)
