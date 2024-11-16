FROM oven/bun:latest

WORKDIR /app/next-app

COPY package.json ./
COPY bun.lockb ./

RUN bun install

COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

CMD bun run dev
