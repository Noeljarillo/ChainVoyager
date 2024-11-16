"use client";

import { cookieToInitialState, WagmiProvider } from "wagmi";
import { darkTheme, RainbowKitProvider } from "@rainbow-me/rainbowkit";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

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

const API_ENDPOINT = process.env["NEXT_PUBLIC_API_URL"] + "/chat";

const CustomModelAdapter: ChatModelAdapter = {
  async *run({ messages, abortSignal }) {
    const result = await fetch(API_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages,
      }),
      signal: abortSignal,
    });
    const { data } = await result.json();

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

export default function Providers({ children, cookie }: Props) {
  const initialState = cookieToInitialState(config, cookie);
  const runtime = useLocalRuntime(CustomModelAdapter);

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
          <AssistantRuntimeProvider runtime={runtime}>
            {children}
          </AssistantRuntimeProvider>
        </RainbowKitProvider>
      </QueryClientProvider>
    </WagmiProvider>
  );
}
