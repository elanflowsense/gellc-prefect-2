FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including git for GitHub deployments
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check --no-warn-script-location -r requirements.txt

# Copy your Prefect flows and code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PREFECT_MODE=flow

# Make startup script executable
RUN chmod +x start.sh

# Default command - uses startup script for flexibility
CMD ["./start.sh"]