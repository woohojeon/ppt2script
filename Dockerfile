FROM python:3.11-slim

# Install LibreOffice and system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-writer \
    libreoffice-impress \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else
COPY . .

# Create necessary directories
RUN mkdir -p uploads outputs templates

# Expose port
EXPOSE 8080

# Set environment variable for PORT
ENV PORT=8080

# Start command - gunicorn will bind to the PORT env variable
CMD gunicorn web_app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 300
