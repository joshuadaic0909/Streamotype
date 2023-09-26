FROM python:3.8-slim

RUN apt-get update && apt-get install -y nginx && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY nginx.conf /etc/nginx/sites-available/default

CMD service nginx start && gunicorn run:app -b 127.0.0.1:8000
