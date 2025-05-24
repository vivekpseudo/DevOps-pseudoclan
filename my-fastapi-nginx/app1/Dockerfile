# app1/Dockerfile
FROM python:3.10-slim AS base

# Install FastAPI app dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app /app/app

# Start FastAPI in background
CMD uvicorn app.main:app --host 127.0.0.1 --port 8000 & \
    nginx -g "daemon off;"

# Install nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean

# Copy nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

EXPOSE 80
