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

# Expose HTTP port
EXPOSE 8000

# Run the server using HTTP transport on port 8000
CMD ["python", "main.py", "run", "--transport", "http", "--port", "8000"]