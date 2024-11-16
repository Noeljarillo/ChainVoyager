import { z } from "zod";
import { NextRequest, NextResponse } from "next/server";

const schema = z.object({
  prompt: z.unknown(),
  wallet: z.string(),
});

const API_ENDPOINT = process.env["NEXT_PUBLIC_API_URL"] + "/chat";

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

  const { prompt, wallet } = parsed.data;

  const aiRequest = await fetch(API_ENDPOINT, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({
      prompt,
      wallet,
    }),
  });

  if (!aiRequest.ok) {
    return NextResponse.json({
      message: "Failed to fetch data from AI server.",
      context: await aiRequest.text(),
    }, {
      status: 500,
    });
  }

  const aiResponse = await aiRequest.json();

  return NextResponse.json(aiResponse);
}
