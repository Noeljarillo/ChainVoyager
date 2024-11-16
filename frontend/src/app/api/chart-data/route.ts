import { z } from "zod";
import { NextRequest, NextResponse } from "next/server";

const schema = z.object({
  wallet: z.string(),
  chain_id: z.string(),
});

const API_ENDPOINT = process.env["NEXT_PUBLIC_API_URL"] + "/get_chart_data";

export async function POST(request: NextRequest) {
  const body = await request.json();
  const parsed = await schema.safeParseAsync(body);

  if (parsed.error) {
    return NextResponse.json({
      error: "Invalid request body.",
    }, {
      status: 400,
    });
  }

  const { wallet, chain_id } = parsed.data;

  const chartRequest = await fetch(API_ENDPOINT, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({
      wallet,
      chain_id,
      timerange: "1year",
    }),
  });

  if (!chartRequest.ok) {
    return NextResponse.json({
      message: "Failed to fetch data from AI server.",
      context: await chartRequest.text(),
    }, {
      status: 500,
    });
  }

  const chartResponse = await chartRequest.json() as {
    result: {
      timestamp: number;
      value_usd: number;
    }[];
  };

  const aggregatedByMonth = chartResponse.result.reduce<{
    [key: string]: {
      total: number;
      count: number;
      average: number;
    };
  }>((acc, curr) => {
    const date = new Date(curr.timestamp * 1000);
    const year = date.getFullYear();

    const key = `${date.toLocaleString("default", { month: "short" })} ${year}`;

    if (!acc[key]) {
      acc[key] = {
        total: 0,
        count: 0,
        average: 0,
      };
    }

    acc[key].count += 1;
    acc[key].total += curr.value_usd;
    acc[key].average = acc[key].total / acc[key].count;

    return acc;
  }, {});

  return NextResponse.json(
    Object.fromEntries(
      Object.entries(aggregatedByMonth).map(([key, value]) => [
        key,
        {
          average: value.average,
        },
      ]),
    ),
  );
}
