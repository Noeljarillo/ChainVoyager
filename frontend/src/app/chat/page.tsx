"use client";
import ChatThread from "@/components/chat-thread";
import { IconChartBar } from "@tabler/icons-react";
import { useContext, useEffect } from "react";
import { GraphContext } from "@/app/providers";
import { BarChartComponent } from "@/components/bar-chart";
import { PieChartComponent } from "@/components/pie-chart";
import { AreaChartComponent } from "@/components/area-chart";
import { useAccount } from "wagmi";

type ExtractFromContext<T> = T extends React.Context<infer U> ? U : never;

export default function ChatComponent() {
  const { graphs } = useContext(GraphContext);
  const { isConnected } = useAccount();
  const links = [
    {
      label: "Charts",
      href: "#",
      icon: (
        <IconChartBar className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
      ),
    },
  ];

  useEffect(() => {
    if (!isConnected) {
      window.location.href = "/";
    }
  }, [isConnected]);

  const graphKeyToComponent: {
    [key in ExtractFromContext<typeof GraphContext>["graphs"][number]]:
      React.ReactNode;
  } = {
    "bar": <BarChartComponent />,
    "line": <AreaChartComponent />,
    "pie": <PieChartComponent />,
  };

  return (
    <ChatThread
      links={links}
      graphs={graphs.map(
        (graph) => graphKeyToComponent[graph],
      )}
    />
  );
}
