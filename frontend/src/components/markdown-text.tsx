"use client";
import {
  makeMarkdownText,
  MarkdownTextPrimitiveProps,
} from "@assistant-ui/react-markdown";
import { useContentPartText } from "@assistant-ui/react";
import { useContext, useEffect } from "react";
import { GraphContext } from "@/app/providers";

export default function CustomMarkdownText(props: MarkdownTextPrimitiveProps) {
  const { graphs, setGraphs } = useContext(GraphContext);
  const { status } = useContentPartText();

  useEffect(() => {
    if (status.type === "complete" && graphs.length === 0) {
      setGraphs(["pie", "bar", "line"]);
    }
  }, [status, graphs.length, setGraphs]);

  const MarkdownText = makeMarkdownText(props);

  return <MarkdownText />;
}
