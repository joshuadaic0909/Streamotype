FROM --platform=$TARGETPLATFORM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    docker \
    nginx \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# Copy the app
COPY . /app/
RUN chmod +x /app/entrypoint.sh

EXPOSE 14000-14100
EXPOSE 5000
EXPOSE 80


ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD []