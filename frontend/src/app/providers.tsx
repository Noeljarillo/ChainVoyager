"use client";

import { cookieToInitialState, WagmiProvider } from "wagmi";
import { darkTheme, RainbowKitProvider } from "@rainbow-me/rainbowkit";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createContext, useState } from "react";

import { config } from "@/lib/config";

import {
  AssistantRuntimeProvider,
  type ChatModelAdapter,
  useLocalRuntime,
} from "@assistant-ui/react";

const queryClient = new QueryClient();

type Props = {
  children: React.ReactNode;
  cookie?: string | null;
};

const CustomModelAdapter: ChatModelAdapter = {
  async *run({ messages, abortSignal }) {
    let data = "";
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        signal: abortSignal,
        body: JSON.stringify({
          prompt: messages.length > 1
            ? {
              context: messages.slice(0, -1),
              prompt: messages[messages.length - 1],
            }
            : messages,
          wallet: localStorage.getItem("wallet"),
        }),
      });
      data = (await res.json())["summary"];
    } catch (error) {
      if (error instanceof Error) {
        data = error.message ?? "Unknown error, please try again later.";
      } else {
        data = "Unknown error, please try again later.";
      }
    }

    const stream: string[] = data.match(/.{1,10}/g) || [];

    let text = "";
    for await (const part of stream) {
      text += part;

      yield {
        content: [{ type: "text", text }],
      };
    }
  },
};

export const GraphContext = createContext<{
  graphs: ("pie" | "line" | "bar")[];
  setGraphs: React.Dispatch<React.SetStateAction<("pie" | "line" | "bar")[]>>;
}>({
  graphs: [],
  setGraphs: () => {},
});

export default function Providers({ children, cookie }: Props) {
  const initialState = cookieToInitialState(config, cookie);
  const runtime = useLocalRuntime(CustomModelAdapter);
  const [graphs, setGraphs] = useState<("pie" | "line" | "bar")[]>([]);

  return (
    <WagmiProvider config={config} initialState={initialState}>
      <QueryClientProvider client={queryClient}>
        <RainbowKitProvider
          theme={darkTheme({
            accentColor: "#0E76FD",
            accentColorForeground: "white",
            borderRadius: "large",
            fontStack: "system",
            overlayBlur: "small",
          })}
        >
          <GraphContext.Provider
            value={{ graphs, setGraphs }}
          >
            <AssistantRuntimeProvider runtime={runtime}>
              {children}
            </AssistantRuntimeProvider>
          </GraphContext.Provider>
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
