"use client";

import ChatThread from "@/components/chat-thread";
import { IconChartBar } from "@tabler/icons-react";
import { useContext, useEffect, useMemo, useState } from "react";
import { GraphContext } from "@/app/providers";
import { BarChartComponent } from "@/components/bar-chart";
import { PieChartComponent } from "@/components/pie-chart";
import { AreaChartComponent } from "@/components/area-chart";
import { useAccount } from "wagmi";

type MonthlyVolumeData = {
  string: {
    total: number;
    count: number;
    average: number;
  };
}[];

type VolumeConfig = Record<string, { label: string; color: string }>;

function useFetchMonthlyVolume() {
  const [data, setData] = useState<MonthlyVolumeData>([]);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("/api/chart-data", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            wallet: localStorage.getItem("wallet"),
            chain_id: "1",
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to fetch chart data");
        }

        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err as Error);
      }
    };

    fetchData();
  }, []);

  return { data, error };
}

const VOLUME_CONFIG: VolumeConfig = {
  average: { label: "Average", color: "#fbbf24" },
};

const GRAPH_COMPONENTS = {
  bar: (data: MonthlyVolumeData) => (
    <BarChartComponent
      data={data}
      config={VOLUME_CONFIG}
      title="Monthly Volume Metrics"
      xAxisKey="month"
    />
  ),
  line: () => <AreaChartComponent />,
  pie: () => <PieChartComponent />,
};

export default function ChatComponent() {
  const { graphs } = useContext(GraphContext);
  const { isConnected } = useAccount();
  const { data: monthlyVolume, error } = useFetchMonthlyVolume();

  useEffect(() => {
    if (!isConnected) {
      window.location.href = "/";
    }
  }, [isConnected]);

  const links = useMemo(
    () => [
      {
        label: "Charts",
        href: "#",
        icon: (
          <IconChartBar className="text-neutral-700 dark:text-neutral-200 h-5 w-5 flex-shrink-0" />
        ),
      },
    ],
    [],
  );

  if (error) {
    return <div>Error loading charts: {error.message}</div>;
  }

  return (
    <ChatThread
      links={links}
      graphs={graphs.map((graph) =>
        GRAPH_COMPONENTS[graph]?.(monthlyVolume) || null
      )}
    />
  );
}
