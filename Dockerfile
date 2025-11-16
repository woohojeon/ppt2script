FROM python:3.11-slim

# Install LibreOffice
RUN apt-get update && \
    apt-get install -y --no-install-recommends libreoffice && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy everything
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p uploads outputs

# Expose port
EXPOSE 8080

# Start command
CMD gunicorn web_app:app --bind 0.0.0.0:$PORT
