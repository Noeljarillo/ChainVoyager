"use client";

import { Cell, Label, Pie, PieChart, Tooltip } from "recharts";
import { ChartConfig, ChartContainer } from "@/components/ui/chart";
import { CardHeader, CardTitle } from "@/components/ui/card";

const chartData = [
  { name: "Ethereum", value: 20.55, color: "#3c3c3d" },
  { name: "USDC", value: 82.19, color: "#2563eb" },
];

const chartConfig = chartData.reduce(
  (acc, coin) => ({
    ...acc,
    [coin.name.toLowerCase().replace(/ /g, "_")]: {
      label: coin.name,
      color: coin.color,
    },
  }),
  {},
) satisfies ChartConfig;

export function PieChartComponent() {
  const totalValue = chartData.reduce((acc, curr) => acc + curr.value, 0);

  return (
    <>
      <CardHeader>
        <CardTitle>Crypto Portfolio Distribution</CardTitle>
      </CardHeader>
      <ChartContainer config={chartConfig} className="h-[200px] w-full">
        <PieChart width={400} height={200}>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            strokeWidth={5}
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
            <Label
              content={({ viewBox }) => {
                if (viewBox && "cx" in viewBox && "cy" in viewBox) {
                  return (
                    <text
                      x={viewBox.cx}
                      y={viewBox.cy}
                      textAnchor="middle"
                      dominantBaseline="middle"
                    >
                      <tspan
                        x={viewBox.cx}
                        y={viewBox.cy}
                        className="fill-foreground text-lg font-bold"
                      >
                        {totalValue}
                      </tspan>
                      <tspan
                        x={viewBox.cx}
                        y={(viewBox.cy || 0) + 20}
                        className="fill-muted-foreground text-sm"
                      >
                        Total USD
                      </tspan>
                    </text>
                  );
                }
              }}
            />
          </Pie>
          <Tooltip />
        </PieChart>
      </ChartContainer>
    </>
  );
}
