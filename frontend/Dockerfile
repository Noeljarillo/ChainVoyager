FROM oven/bun:latest AS builder

WORKDIR /app/next-app

COPY package.json ./
COPY bun.lockb ./

RUN bun install

COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN bun run build

FROM oven/bun:runtime

WORKDIR /app/next-app

COPY --from=builder /app/next-app/.next ./.next
COPY --from=builder /app/next-app/public ./public
COPY --from=builder /app/next-app/package.json ./
COPY --from=builder /app/next-app/bun.lockb ./

RUN bun install --production

CMD ["bun", "run", "start"]
