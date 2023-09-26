# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in docker
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD ["gunicorn", "run:app", "-b", "0.0.0.0:5000"]
