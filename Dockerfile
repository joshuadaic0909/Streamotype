FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "app.py", "--server.headless", "true", "--browser.serverAddress", "0.0.0.0", "--server.port", "8501"]
