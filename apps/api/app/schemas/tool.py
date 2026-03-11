from typing import Any

from pydantic import BaseModel, Field


class ToolPlanItem(BaseModel):
    tool_name: str = Field(min_length=1, description="Planned tool name.")
    args: dict[str, Any] = Field(default_factory=dict, description="Validated tool arguments.")


class ToolCallItem(BaseModel):
    tool_name: str = Field(min_length=1, description="Executed tool name.")
    tool_input: dict[str, Any] = Field(default_factory=dict, description="Tool input payload.")
    tool_output: dict[str, Any] = Field(default_factory=dict, description="Tool output payload.")
