"use client";
import { Area, AreaChart, CartesianGrid, XAxis } from "recharts";
import { ChartConfig, ChartContainer } from "@/components/ui/chart";
import { ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { ChartLegend, ChartLegendContent } from "@/components/ui/chart";
import { CardHeader, CardTitle } from "@/components/ui/card";

const chartData = [
  { month: "January", BTC: 12000, ETH: 8500, ADA: 3000 },
  { month: "February", BTC: 14000, ETH: 10000, ADA: 3200 },
  { month: "March", BTC: 13500, ETH: 9500, ADA: 3100 },
  { month: "April", BTC: 14500, ETH: 11000, ADA: 3500 },
  { month: "May", BTC: 15000, ETH: 12000, ADA: 4000 },
  { month: "June", BTC: 16000, ETH: 13000, ADA: 4500 },
];

const chartConfig = {
  BTC: {
    label: "Bitcoin (BTC)",
    color: "#f59e0b",
  },
  ETH: {
    label: "Ethereum (ETH)",
    color: "#2563eb",
  },
  ADA: {
    label: "Cardano (ADA)",
    color: "#10b981",
  },
} satisfies ChartConfig;

export function AreaChartComponent() {
  return (
    <>
      <CardHeader>
        <CardTitle>Top 3 Asset Positions Over 6 Months</CardTitle>
      </CardHeader>
      <ChartContainer config={chartConfig} className="h-[200px] w-full">
        <AreaChart accessibilityLayer data={chartData}>
          <CartesianGrid vertical={false} />
          <XAxis
            dataKey="month"
            tickLine={false}
            tickMargin={10}
            axisLine={false}
            tickFormatter={(value) => value.slice(0, 3)}
          />
          <ChartTooltip content={<ChartTooltipContent />} />
          <ChartLegend content={<ChartLegendContent />} />
          <Area
            type="monotone"
            dataKey="BTC"
            stackId="1"
            stroke={chartConfig.BTC.color}
            fill={chartConfig.BTC.color}
            fillOpacity={0.6}
          />
          <Area
            type="monotone"
            dataKey="ETH"
            stackId="1"
            stroke={chartConfig.ETH.color}
            fill={chartConfig.ETH.color}
            fillOpacity={0.6}
          />
          <Area
            type="monotone"
            dataKey="ADA"
            stackId="1"
            stroke={chartConfig.ADA.color}
            fill={chartConfig.ADA.color}
            fillOpacity={0.6}
          />
        </AreaChart>
      </ChartContainer>
    </>
  );
}
