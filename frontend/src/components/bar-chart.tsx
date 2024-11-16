"use client";
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts";
import { ChartConfig, ChartContainer } from "@/components/ui/chart";
import { ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { ChartLegend, ChartLegendContent } from "@/components/ui/chart";
import { CardHeader, CardTitle } from "@/components/ui/card";

const chartData = [
  { month: "January", usdIn: 10000, usdOut: 8000 },
  { month: "February", usdIn: 12000, usdOut: 9500 },
  { month: "March", usdIn: 15000, usdOut: 11000 },
  { month: "April", usdIn: 8000, usdOut: 7000 },
  { month: "May", usdIn: 11000, usdOut: 9000 },
  { month: "June", usdIn: 13000, usdOut: 12000 },
];

const chartConfig = {
  usdIn: {
    label: "USD In",
    color: "#22c55e",
  },
  usdOut: {
    label: "USD Out",
    color: "#ef4444",
  },
} satisfies ChartConfig;

export function BarChartComponent() {
  return (
    <>
      <CardHeader>
        <CardTitle>Monthly USD In and Out</CardTitle>
      </CardHeader>
      <ChartContainer config={chartConfig} className="h-[200px] w-full">
        <BarChart accessibilityLayer data={chartData}>
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
          <Bar dataKey="usdIn" fill={chartConfig.usdIn.color} radius={4} />
          <Bar dataKey="usdOut" fill={chartConfig.usdOut.color} radius={4} />
        </BarChart>
      </ChartContainer>
    </>
  );
}
