# Multi-stage build for Next.js frontend
# Builder stage
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json .
COPY package-lock.json .

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Runner stage
FROM node:18-alpine AS runner
ENV HOSTNAME="0.0.0.0"

# Set working directory
WORKDIR /app

# Copy the standalone output from builder stage
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Expose port 3000
EXPOSE 3000

# Set environment variable to ensure server listens on all interfaces
ENV HOSTNAME=0.0.0.0
ENV HOST=0.0.0.0
ENV NEXT_HOST=0.0.0.0

# Start the application
CMD ["node", "server.js"]