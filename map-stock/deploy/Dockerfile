# Use Alpine as base image with Python 3.9
FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Install system dependencies required to compile Python packages
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Copy requirements file
COPY requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r ./requirements.txt
    
