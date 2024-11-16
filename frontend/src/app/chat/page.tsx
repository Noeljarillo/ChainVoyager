"use client";
import Navbar from "@/components/floating-navbar";
import { Thread } from "@assistant-ui/react";
import "@assistant-ui/react/styles/index.css";
import { MarkdownText } from "@/components/ui/markdown-to-text";

export default function ChatPage() {
  return (
    <>
      <Navbar alwaysVisible />
      <div className="h-full">
        <Thread assistantMessage={{ components: { Text: MarkdownText } }} />
      </div>
    </>
  );
}
