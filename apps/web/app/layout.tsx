import type { Metadata } from "next";

import "./globals.css";
import { QueryProvider } from "@/components/layout/query-provider";

export const metadata: Metadata = {
  title: "Agent Workspace",
  description: "Task-driven AI agent workspace v1",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="font-sans antialiased">
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
