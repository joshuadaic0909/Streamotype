# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Set the working directory in docker
WORKDIR /usr/src/app

# Copy the content of the local src directory to the working directory
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Run app.py when the container launches
CMD ["sh", "-c", "service nginx start && gunicorn --bind 0.0.0.0:8000 run:app"]
