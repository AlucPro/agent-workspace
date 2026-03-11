"use client";

import { FormEvent, useState } from "react";

import { useChat } from "@/hooks/use-chat";
import type { SourceItem, ToolCallItem, TraceItem, UiMessage } from "@/types/chat";

function PanelTitle({
  eyebrow,
  title,
  detail,
}: {
  eyebrow: string;
  title: string;
  detail: string;
}) {
  return (
    <div className="space-y-2">
      <p className="text-xs font-medium uppercase tracking-[0.28em] text-accent">{eyebrow}</p>
      <div className="space-y-1">
        <h2 className="text-2xl font-semibold tracking-tight text-ink">{title}</h2>
        <p className="max-w-xl text-sm text-muted">{detail}</p>
      </div>
    </div>
  );
}

function MessageCard({ message }: { message: UiMessage }) {
  const isUser = message.role === "user";

  return (
    <article
      className={`rounded-[28px] border px-5 py-4 shadow-panel transition ${
        isUser ? "ml-auto max-w-2xl border-ink bg-ink text-paper" : "max-w-3xl border-line bg-panel"
      }`}
    >
      <div className="mb-3 flex items-center justify-between gap-3">
        <span className="text-xs font-medium uppercase tracking-[0.24em] text-current/70">
          {isUser ? "User Task" : "Agent Reply"}
        </span>
        {message.response?.intent ? (
          <span
            className={`rounded-full px-3 py-1 text-xs font-medium ${
              isUser ? "bg-paper/15 text-paper" : "bg-accentSoft text-ink"
            }`}
          >
            {message.response.intent}
          </span>
        ) : null}
      </div>
      <p className="whitespace-pre-wrap text-sm leading-7">{message.content}</p>
    </article>
  );
}

function SourcesPanel({ sources }: { sources: SourceItem[] }) {
  return (
    <section className="rounded-[24px] border border-line bg-panel p-5 shadow-panel">
      <h3 className="text-sm font-semibold uppercase tracking-[0.24em] text-muted">Sources</h3>
      <div className="mt-4 space-y-3">
        {sources.length === 0 ? (
          <p className="text-sm text-muted">当前消息没有知识库引用。</p>
        ) : (
          sources.map((source) => (
            <article key={source.chunk_id} className="rounded-2xl border border-line bg-white/70 p-4">
              <div className="flex items-center justify-between gap-4 text-xs uppercase tracking-[0.22em] text-muted">
                <span>{source.file_name}</span>
                <span>{source.chunk_id}</span>
              </div>
              <p className="mt-3 text-sm leading-6 text-ink">{source.content}</p>
            </article>
          ))
        )}
      </div>
    </section>
  );
}

function ToolCallsPanel({ toolCalls }: { toolCalls: ToolCallItem[] }) {
  return (
    <section className="rounded-[24px] border border-line bg-panel p-5 shadow-panel">
      <h3 className="text-sm font-semibold uppercase tracking-[0.24em] text-muted">Tool Calls</h3>
      <div className="mt-4 space-y-3">
        {toolCalls.length === 0 ? (
          <p className="text-sm text-muted">当前消息没有触发工具调用。</p>
        ) : (
          toolCalls.map((toolCall, index) => (
            <article key={`${toolCall.tool_name}_${index}`} className="rounded-2xl border border-line bg-white/70 p-4">
              <div className="text-sm font-semibold text-ink">{toolCall.tool_name}</div>
              <pre className="mt-3 overflow-x-auto rounded-xl bg-ink p-3 text-xs text-paper">
                {JSON.stringify(toolCall, null, 2)}
              </pre>
            </article>
          ))
        )}
      </div>
    </section>
  );
}

function TracePanel({ trace }: { trace: TraceItem[] }) {
  return (
    <section className="rounded-[24px] border border-line bg-panel p-5 shadow-panel">
      <h3 className="text-sm font-semibold uppercase tracking-[0.24em] text-muted">Trace</h3>
      <ol className="mt-4 space-y-3">
        {trace.length === 0 ? (
          <li className="text-sm text-muted">当前消息没有 trace 记录。</li>
        ) : (
          trace.map((item, index) => (
            <li key={`${item.step}_${index}`} className="flex gap-3 text-sm leading-6 text-ink">
              <span className="mt-0.5 inline-flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-accent text-xs font-semibold text-paper">
                {index + 1}
              </span>
              <span>{item.step}</span>
            </li>
          ))
        )}
      </ol>
    </section>
  );
}

export function ChatShell() {
  const [draft, setDraft] = useState("");
  const { examplePrompts, isPending, messages, sendMessage, setUseKnowledgeBase, useKnowledgeBase, error } =
    useChat();
  const selectedAssistantMessage = [...messages].reverse().find((message) => message.role === "assistant");

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const message = draft.trim();
    if (!message || isPending) {
      return;
    }

    sendMessage(message);
    setDraft("");
  };

  return (
    <main className="min-h-screen px-4 py-6 md:px-6 lg:px-8">
      <div className="mx-auto grid max-w-[1600px] gap-6 xl:grid-cols-[260px_minmax(0,1fr)_360px]">
        <aside className="rounded-[32px] border border-line bg-panel/95 p-6 shadow-panel">
          <PanelTitle
            eyebrow="Sessions"
            title="Chat Workspace"
            detail="v1 先展示单会话布局，后续再接会话列表与持久化。"
          />
          <div className="mt-8 rounded-[24px] border border-dashed border-line bg-white/70 p-4">
            <div className="text-xs uppercase tracking-[0.2em] text-muted">Current Session</div>
            <div className="mt-2 text-lg font-semibold text-ink">Agent Demo Run</div>
            <p className="mt-2 text-sm leading-6 text-muted">
              当前已完成文档要求的聊天主界面、trace 面板和 sources/tool calls 展示结构。
            </p>
          </div>
          <div className="mt-8 space-y-3">
            <div className="text-xs uppercase tracking-[0.2em] text-muted">Prompt Starters</div>
            {examplePrompts.map((prompt) => (
              <button
                key={prompt}
                type="button"
                onClick={() => setDraft(prompt)}
                className="w-full rounded-2xl border border-line bg-white/70 px-4 py-3 text-left text-sm leading-6 text-ink transition hover:border-accent hover:bg-panel"
              >
                {prompt}
              </button>
            ))}
          </div>
        </aside>

        <section className="rounded-[32px] border border-line bg-panel/95 p-6 shadow-panel">
          <PanelTitle
            eyebrow="Chat"
            title="Task-first Agent UI"
            detail="按照 v1 文档，主区先承载消息流与输入框。当前未联通后端时，会自动回退到 mock 响应。"
          />

          <div className="mt-8 flex items-center justify-between gap-4 rounded-[24px] border border-line bg-white/70 px-4 py-3">
            <label className="flex items-center gap-3 text-sm text-ink">
              <input
                type="checkbox"
                checked={useKnowledgeBase}
                onChange={(event) => setUseKnowledgeBase(event.target.checked)}
                className="h-4 w-4 rounded border-line text-accent focus:ring-accent"
              />
              开启知识库问答模式
            </label>
            <span className="text-xs uppercase tracking-[0.24em] text-muted">
              {isPending ? "Agent is thinking" : "Ready"}
            </span>
          </div>

          <div className="mt-6 space-y-4">
            {messages.map((message) => (
              <MessageCard key={message.id} message={message} />
            ))}
            {isPending ? (
              <div className="max-w-3xl rounded-[28px] border border-line bg-white/75 px-5 py-4 text-sm text-muted shadow-panel">
                正在等待 Agent 响应...
              </div>
            ) : null}
          </div>

          <form onSubmit={handleSubmit} className="mt-8 rounded-[28px] border border-line bg-white/85 p-4 shadow-panel">
            <label htmlFor="message" className="text-xs font-medium uppercase tracking-[0.24em] text-muted">
              New Task
            </label>
            <textarea
              id="message"
              rows={5}
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              placeholder="输入你的任务，例如：帮我计算 2025 年同比增长率，去年收入 120 万，今年 156 万"
              className="mt-3 w-full resize-none border-0 bg-transparent text-sm leading-7 text-ink outline-none placeholder:text-muted"
            />
            <div className="mt-4 flex items-center justify-between gap-4">
              <p className="text-sm text-muted">
                {error ? `请求失败，已回退 mock：${error}` : "默认请求 http://localhost:8000/api/chat"}
              </p>
              <button
                type="submit"
                disabled={isPending || draft.trim().length === 0}
                className="rounded-full bg-ink px-5 py-3 text-sm font-medium text-paper transition hover:bg-accent disabled:cursor-not-allowed disabled:bg-muted"
              >
                发送任务
              </button>
            </div>
          </form>
        </section>

        <aside className="space-y-6">
          <section className="rounded-[32px] border border-line bg-panel/95 p-6 shadow-panel">
            <PanelTitle
              eyebrow="Inspector"
              title="Execution Detail"
              detail="每条 Agent 回复保留 Final Answer、Sources、Tool Calls、Trace 四块展示位。"
            />
          </section>
          <SourcesPanel sources={selectedAssistantMessage?.response?.sources ?? []} />
          <ToolCallsPanel toolCalls={selectedAssistantMessage?.response?.tool_calls ?? []} />
          <TracePanel trace={selectedAssistantMessage?.response?.trace ?? []} />
        </aside>
      </div>
    </main>
  );
}
