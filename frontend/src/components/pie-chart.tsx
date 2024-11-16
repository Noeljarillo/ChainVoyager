"use client";

import { Cell, Label, Pie, PieChart, Tooltip } from "recharts";
import { ChartConfig, ChartContainer } from "@/components/ui/chart";
import { CardHeader, CardTitle } from "@/components/ui/card";

const chartData = [
  { name: "Bitcoin", value: 45000, color: "#f7931a" },
  { name: "Ethereum", value: 30000, color: "#3c3c3d" },
  { name: "Binance Coin", value: 15000, color: "#f0b90b" },
  { name: "Cardano", value: 10000, color: "#0033ad" },
  { name: "Solana", value: 8000, color: "#00ffa1" },
  { name: "Polkadot", value: 7000, color: "#e6007a" },
  { name: "Dogecoin", value: 6000, color: "#c2a633" },
  { name: "XRP", value: 5000, color: "#00aaee" },
  { name: "Litecoin", value: 4000, color: "#b8b8b8" },
  { name: "Chainlink", value: 3500, color: "#2a5ada" },
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
