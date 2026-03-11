const demoDocuments = [
  {
    id: "doc_v1",
    fileName: "Agent Workspace v1 技术设计文档.md",
    status: "processed",
    chunkCount: 12,
  },
  {
    id: "doc_jd",
    fileName: "sample-jd.pdf",
    status: "pending",
    chunkCount: 0,
  },
];

export default function DocumentsPage() {
  return (
    <main className="min-h-screen px-4 py-6 md:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl space-y-6">
        <section className="rounded-[32px] border border-line bg-panel/95 p-6 shadow-panel">
          <p className="text-xs font-medium uppercase tracking-[0.28em] text-accent">Documents</p>
          <div className="mt-3 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
            <div>
              <h1 className="text-3xl font-semibold tracking-tight text-ink">Knowledge Base Console</h1>
              <p className="mt-2 max-w-2xl text-sm leading-7 text-muted">
                这是按 v1 文档预留的文档页。当前提供上传入口与列表 UI，占位后续的上传、切分、向量化与状态刷新流程。
              </p>
            </div>
            <button
              type="button"
              className="rounded-full bg-ink px-5 py-3 text-sm font-medium text-paper transition hover:bg-accent"
            >
              上传文档
            </button>
          </div>
        </section>

        <section className="rounded-[32px] border border-line bg-panel/95 p-6 shadow-panel">
          <div className="grid gap-4 md:grid-cols-2">
            {demoDocuments.map((document) => (
              <article key={document.id} className="rounded-[24px] border border-line bg-white/75 p-5">
                <div className="flex items-center justify-between gap-3">
                  <span className="text-xs uppercase tracking-[0.24em] text-muted">{document.id}</span>
                  <span className="rounded-full bg-accentSoft px-3 py-1 text-xs font-medium text-ink">
                    {document.status}
                  </span>
                </div>
                <h2 className="mt-4 text-lg font-semibold text-ink">{document.fileName}</h2>
                <p className="mt-3 text-sm text-muted">chunk count: {document.chunkCount}</p>
              </article>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
