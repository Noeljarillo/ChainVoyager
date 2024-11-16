"use client";
import { Bar, BarChart, CartesianGrid, XAxis } from "recharts";
import { ChartConfig, ChartContainer } from "@/components/ui/chart";
import { ChartTooltip, ChartTooltipContent } from "@/components/ui/chart";
import { ChartLegend, ChartLegendContent } from "@/components/ui/chart";
import { CardHeader, CardTitle } from "@/components/ui/card";

type GenericBarChartProps<T extends object> = {
  data: T[];
  config: ChartConfig;
  title: string;
  xAxisKey: string;
};

export function BarChartComponent<T extends object>({
  data,
  config,
  title,
  xAxisKey,
}: GenericBarChartProps<T>) {
  const transformedData = Object.entries(data).map(([key, value]) => ({
    [xAxisKey]: key,
    ...value,
  }));

  return (
    <>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <ChartContainer config={config} className="h-[200px] w-full">
        <BarChart accessibilityLayer data={transformedData}>
          <CartesianGrid vertical={false} />
          <XAxis
            dataKey={xAxisKey as string}
            tickLine={false}
            tickMargin={10}
            axisLine={false}
            tickFormatter={(value) => String(value).slice(0, 3)}
          />
          <ChartTooltip content={<ChartTooltipContent />} />
          <ChartLegend content={<ChartLegendContent />} />
          {Object.entries(config).map(([key, { label, color }]) => (
            <Bar
              key={key}
              dataKey={key}
              fill={color}
              name={String(label)}
              radius={4}
            />
          ))}
        </BarChart>
      </ChartContainer>
    </>
  );
}
