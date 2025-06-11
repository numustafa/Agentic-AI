# Dockerfile for a development container with Python, Node.js, and uv

# Based on Python 3.11 image with slim variant for a smaller footprint
FROM python:3.11-slim 

# Set environment variables to optimize Python performance and behavior 
ENV PYTHONUNBUFFERED=true \
    PYTHONDONTWRITEBYTECODE=true \
    PIP_NO_CACHE_DIR=true \
    PIP_DISABLE_PIP_VERSION_CHECK=true

# Install system dependencies with minimal packages and active cleaning to reduce image size.
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (Week 0 requirement)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install uv (modern Python package manager) 
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /workspace

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash vscode \
    && chown -R vscode:vscode /workspace
USER vscode

# Default command
CMD ["/bin/bash"]