import type { ChatResponse } from "@/types/chat";

interface ChatRequest {
  session_id: string;
  message: string;
  use_knowledge_base: boolean;
}

const mockResponse = (request: ChatRequest): ChatResponse => ({
  session_id: request.session_id,
  message_id: `msg_${Date.now()}`,
  intent: request.use_knowledge_base ? "knowledge_qa" : "direct_answer",
  answer: request.use_knowledge_base
    ? "这是前端初始化阶段的 mock 响应。接入后端后，这里会展示基于知识库片段生成的回答。"
    : "这是前端初始化阶段的 mock 响应。下一步可以直接对接 FastAPI 的 /api/chat。",
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
    `input_received: ${request.message.slice(0, 48)}`,
    `intent_detected: ${request.use_knowledge_base ? "knowledge_qa" : "direct_answer"}`,
    "mock_response_generated",
  ],
});

export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
  try {
    const response = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Request failed with ${response.status}`);
    }

    return (await response.json()) as ChatResponse;
  } catch {
    await new Promise((resolve) => setTimeout(resolve, 450));
    return mockResponse(request);
  }
}
