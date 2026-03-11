export type IntentType = "direct_answer" | "knowledge_qa" | "tool_call";

export interface SourceItem {
  document_id: string;
  file_name: string;
  chunk_id: string;
  content: string;
}

export interface ToolCallItem {
  tool_name: string;
  tool_input: Record<string, string | number | boolean>;
  tool_output: Record<string, string | number | boolean>;
}

export interface TraceItem {
  step: string;
}

export interface ChatResponse {
  session_id: string;
  message_id: string;
  intent: IntentType;
  answer: string;
  sources: SourceItem[];
  tool_calls: ToolCallItem[];
  trace: TraceItem[];
}

export interface UiMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  response?: ChatResponse;
}
