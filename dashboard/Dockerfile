FROM python:3.10-slim

WORKDIR /app

# Inline installs with timeouts for reliability
RUN pip install --no-cache-dir --default-timeout=100 --retries=10 flask openai
RUN pip install --no-cache-dir --default-timeout=100 --retries=10 chromadb
RUN pip install --no-cache-dir --default-timeout=100 --retries=10 sentence-transformers

COPY . .

CMD ["python", "app.py"]
