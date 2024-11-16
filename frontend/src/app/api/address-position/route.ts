import { z } from "zod";
import { NextRequest, NextResponse } from "next/server";

const schema = z.object({
  chain_id: z.unknown(),
  wallet_address: z.string(),
});

const API_ENDPOINT = process.env["NEXT_PUBLIC_API_URL"] +
  "/get_address_positions";

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

  const { chain_id, wallet_address } = parsed.data;

  const response = await fetch(API_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      chain_id,
      wallet: wallet_address,
    }),
  });

  if (!response.ok) {
    return NextResponse.error();
  }

  const data = await response.json();

  return NextResponse.json(data);
}
