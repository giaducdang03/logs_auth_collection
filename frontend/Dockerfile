# Build stage
FROM node:18-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

RUN npm install -g serve

COPY --from=builder /app/dist ./dist

# Allow serving the same build from /app/* paths (for VITE_BASE_PATH=/app/)
RUN ln -s . /app/dist/app

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]
