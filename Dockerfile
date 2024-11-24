# Dockerfile
FROM python:3.11-slim

WORKDIR /workspace

# Install essential packages
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Keep container running
CMD ["bash"]
