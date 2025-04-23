# Base image with Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y nano
RUN apt-get update && apt-get install -y vim

# Copy project files
COPY . .