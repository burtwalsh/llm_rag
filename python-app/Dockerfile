FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY kafka/ ./kafka/
COPY rag/ ./rag/

CMD ["python", "kafka/producer.py"]
