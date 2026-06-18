# Use the requested python-3.13.3-slim base image
FROM python:3.13.3-slim

# Set work directory
WORKDIR /app

# Install system dependencies if any library needs compilation (e.g. lxml, pandas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY main.py .
COPY src/ ./src/

# Expose any ports if fastmcp is ever configured to run on sse (default is stdio for MCP, but good practice)
EXPOSE 8000

# Set entry point to run the MCP server
CMD ["python", "main.py", "run"]
