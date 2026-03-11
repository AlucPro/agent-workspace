import type { ChatResponse, IntentType, SourceItem, ToolCallItem, TraceItem } from "@/types/chat";

export interface ChatRequest {
  session_id: string;
  message: string;
  use_knowledge_base: boolean;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const ENABLE_MOCK_FALLBACK = process.env.NEXT_PUBLIC_ENABLE_CHAT_MOCK === "true";
const VALID_INTENTS: IntentType[] = ["direct_answer", "knowledge_qa", "tool_call"];

function isSourceItem(value: unknown): value is SourceItem {
  if (!value || typeof value !== "object") {
    return false;
  }

  const candidate = value as Record<string, unknown>;
  return (
    typeof candidate.document_id === "string" &&
    typeof candidate.file_name === "string" &&
    typeof candidate.chunk_id === "string" &&
    typeof candidate.content === "string"
  );
}

function isToolCallItem(value: unknown): value is ToolCallItem {
  if (!value || typeof value !== "object") {
    return false;
  }

  const candidate = value as Record<string, unknown>;
  return (
    typeof candidate.tool_name === "string" &&
    typeof candidate.tool_input === "object" &&
    candidate.tool_input !== null &&
    typeof candidate.tool_output === "object" &&
    candidate.tool_output !== null
  );
}

function isTraceItem(value: unknown): value is TraceItem {
  if (!value || typeof value !== "object") {
    return false;
  }

  return typeof (value as Record<string, unknown>).step === "string";
}

function isChatResponse(value: unknown): value is ChatResponse {
  if (!value || typeof value !== "object") {
    return false;
  }

  const candidate = value as Record<string, unknown>;
  return (
    typeof candidate.session_id === "string" &&
    typeof candidate.message_id === "string" &&
    typeof candidate.answer === "string" &&
    typeof candidate.intent === "string" &&
    VALID_INTENTS.includes(candidate.intent as IntentType) &&
    Array.isArray(candidate.sources) &&
    candidate.sources.every(isSourceItem) &&
    Array.isArray(candidate.tool_calls) &&
    candidate.tool_calls.every(isToolCallItem) &&
    Array.isArray(candidate.trace) &&
    candidate.trace.every(isTraceItem)
  );
}

function mockResponse(request: ChatRequest): ChatResponse {
  return {
    session_id: request.session_id,
    message_id: `msg_${Date.now()}`,
    intent: request.use_knowledge_base ? "knowledge_qa" : "direct_answer",
    answer: request.use_knowledge_base
      ? "这是前端 mock 回答。当前未连接后端时，会展示基于知识库模式的占位响应。"
      : "这是前端 mock 回答。当前未连接后端时，会展示 direct answer 模式的占位响应。",
    sources: request.use_knowledge_base
      ? [
          {
            document_id: "doc_v1",
            file_name: "Agent Workspace v1 技术设计文档.md",
            chunk_id: "chunk_01",
            content: "前端技术选型包括 Next.js、TypeScript、Tailwind CSS、React Query。",
          },
        ]
      : [],
    tool_calls: [],
    trace: [
      { step: `input_received: ${request.message.slice(0, 48)}` },
      { step: `intent_detected: ${request.use_knowledge_base ? "knowledge_qa" : "direct_answer"}` },
      { step: "mock_response_generated" },
    ],
  };
}

export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 15_000);

  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
      signal: controller.signal,
    });

    if (!response.ok) {
      throw new Error(`Request failed with ${response.status}`);
    }

    const payload: unknown = await response.json();
    if (!isChatResponse(payload)) {
      throw new Error("Invalid /api/chat response shape");
    }

    return payload;
  } catch (error) {
    if (ENABLE_MOCK_FALLBACK) {
      await new Promise((resolve) => setTimeout(resolve, 450));
      return mockResponse(request);
    }

    if (error instanceof Error && error.name === "AbortError") {
      throw new Error("Request timeout after 15s");
    }

    throw error instanceof Error ? error : new Error("Unknown chat request error");
  } finally {
    window.clearTimeout(timeout);
  }
}
