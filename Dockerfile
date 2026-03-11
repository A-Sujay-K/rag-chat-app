FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PDF parsing
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

