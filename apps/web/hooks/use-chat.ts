"use client";

import { useMutation } from "@tanstack/react-query";
import { useState } from "react";

import { sendChatMessage } from "@/lib/chat";
import type { UiMessage } from "@/types/chat";

const DEFAULT_PROMPTS = [
  "帮我把这段需求整理成开发任务列表",
  "总结这份 PRD 里的核心目标，并列出风险点",
  "帮我计算 2025 年同比增长率，去年收入 120 万，今年 156 万",
];

export function useChat() {
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const [useKnowledgeBase, setUseKnowledgeBase] = useState(true);
  const [requestError, setRequestError] = useState<string | null>(null);
  const [messages, setMessages] = useState<UiMessage[]>([
    {
      id: "assistant_welcome",
      role: "assistant",
      content:
        "欢迎来到 Agent Workspace v1。当前界面已完成前端初始化，支持聊天、trace、sources 和 tool calls 的展示骨架。",
      response: {
        session_id: "session_bootstrap",
        message_id: "assistant_welcome",
        intent: "direct_answer",
        answer:
          "欢迎来到 Agent Workspace v1。当前界面已完成前端初始化，支持聊天、trace、sources 和 tool calls 的展示骨架。",
        sources: [],
        tool_calls: [],
        trace: [{ step: "ui_bootstrapped" }, { step: "ready_for_api_integration" }],
      },
    },
  ]);

  const mutation = useMutation({
    mutationFn: (message: string) =>
      sendChatMessage({
        session_id: sessionId,
        message,
        use_knowledge_base: useKnowledgeBase,
      }),
    onMutate: (message) => {
      setRequestError(null);
      setMessages((current) => [
        ...current,
        {
          id: `user_${Date.now()}`,
          role: "user",
          content: message,
        },
      ]);
    },
    onSuccess: (response) => {
      setMessages((current) => [
        ...current,
        {
          id: response.message_id,
          role: "assistant",
          content: response.answer,
          response,
        },
      ]);
    },
    onError: (error) => {
      setRequestError(error instanceof Error ? error.message : "Chat request failed");
    },
  });

  return {
    examplePrompts: DEFAULT_PROMPTS,
    isPending: mutation.isPending,
    messages,
    sendMessage: mutation.mutate,
    setUseKnowledgeBase,
    useKnowledgeBase,
    error: requestError,
  };
}
