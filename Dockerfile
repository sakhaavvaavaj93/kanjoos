# Stage 1: Build stage for dependencies
FROM debian:bookworm-slim AS builder

# Combine apt commands to reduce layers and clean up cache immediately
RUN sudo apt update && sudo apt install curl
    apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    python3-pip \
    python3-venv \
    ffmpeg \
    && curl -fsSL https://deb.nodesource.com | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files first to leverage layer caching
COPY Installer requirements.txt* ./
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r Installer

# Stage 2: Final runtime stage
FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    ffmpeg \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# Copy only the virtual environment and app code from the builder
COPY --from=builder /opt/venv /opt/venv
COPY . .

ENV PATH="/opt/venv/bin:$PATH"
CMD ["python3", "-m", "modules"]
