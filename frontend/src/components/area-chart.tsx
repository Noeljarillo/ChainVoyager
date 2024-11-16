"use client";

import { Area, AreaChart, CartesianGrid, XAxis } from "recharts";
import { ChartConfig, ChartContainer } from "@/components/ui/chart";
import { ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { ChartLegend, ChartLegendContent } from "@/components/ui/chart";
import { CardHeader, CardTitle } from "@/components/ui/card";
import { useEffect, useState } from "react";

async function fetchChartData() {
  const response = await fetch("/api/address-position", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      chain_id: "1",
      wallet_address: localStorage.getItem("wallet"),
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch chart data");
  }

  return response.json();
}

export function AreaChartComponent() {
  const [chartData, setChartData] = useState<any[]>([]);
  const [chartConfig, setChartConfig] = useState<ChartConfig>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const apiResponse = await fetchChartData();

        const processedData = apiResponse.token.result.map((entry: any) => ({
          month: entry.chain_id || "Unknown",
          profit: entry.abs_profit_usd || 0,
          roi: entry.roi || 0,
        }));

        const dynamicConfig: ChartConfig = {
          profit: { label: "Absolute Profit (USD)", color: "#f59e0b" },
          roi: { label: "ROI", color: "#2563eb" },
        };

        setChartData(processedData);
        setChartConfig(dynamicConfig);
        setLoading(false);
      } catch (err) {
        setError((err as Error).message);
        setLoading(false);
      }
    }

    loadData();
  }, []);

  if (loading) return <div>Loading chart...</div>;
  if (error) return <div>Error loading chart: {error}</div>;

  return (
    <>
      <CardHeader>
        <CardTitle>Dynamic Asset Data</CardTitle>
      </CardHeader>
      <ChartContainer config={chartConfig} className="h-[200px] w-full">
        <AreaChart data={chartData}>
          <CartesianGrid vertical={false} />
          <XAxis
            dataKey="month"
            tickLine={false}
            tickMargin={10}
            axisLine={false}
            tickFormatter={(value) => value.toString().slice(0, 3)}
          />
          <ChartTooltip content={<ChartTooltipContent />} />
          <ChartLegend content={<ChartLegendContent />} />
          {Object.keys(chartConfig).map((key) => (
            <Area
              key={key}
              type="monotone"
              dataKey={key}
              stackId="1"
              stroke={chartConfig[key].color}
              fill={chartConfig[key].color}
              fillOpacity={0.6}
            />
          ))}
        </AreaChart>
      </ChartContainer>
    </>
  );
}
