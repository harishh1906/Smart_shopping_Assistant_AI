# Use official slim Python runtime
FROM python:3.11-slim

# Set environment system flags
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install native system compiler packages for C compilation of mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set standard working directory
WORKDIR /app

# Install dependency files first to leverage Docker build layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend workspaces and catalog databases
COPY backend/ ./backend
COPY database/ ./database

# Expose standard Flask server port
EXPOSE 5000

# Boot modular Flask app controller
CMD ["python", "backend/run.py"]
