# ===========================
# Stage 1: Builder
# ===========================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt


# ===========================
# Stage 2: Runtime
# ===========================
FROM python:3.11-slim

ENV TZ=UTC

WORKDIR /app

# Install cron + timezone data
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron tzdata && \
    ln -sf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create volumes
RUN mkdir -p /data /cron && chmod 755 /data && chmod 755 /cron

# Copy cron job (runs every minute)
COPY cronjob.txt /cron/cronjob.txt
RUN chmod 0644 /cron/cronjob.txt && crontab /cron/cronjob.txt

# Expose API port
EXPOSE 8080

# Start cron + API
CMD service cron start && uvicorn app:app --host 0.0.0.0 --port 8080
