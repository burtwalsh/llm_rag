import psycopg2
from chromadb import Client
from sentence_transformers import SentenceTransformer
import json, os
import requests

print("Starting LLM processor...")

client = Client()
collection = client.get_or_create_collection("stream_samples")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Postgres
conn = psycopg2.connect(
    dbname="ragdb", user="raguser", password="ragpass", host="postgres", port="5432"
)
cursor = conn.cursor()

sample = {"source": "manual-run", "message": "Sensor 42 reports temperature anomaly"}
query = json.dumps(sample)

try:
    results = collection.query(query_embeddings=[model.encode(query).tolist()], n_results=5)
    docs = results["documents"][0]
except IndexError:
    print("No documents in ChromaDB. Skipping inference.")
    exit(0)
except Exception as e:
    print("Unexpected error during ChromaDB query:", e)
    exit(1)

print("Retrieved context docs:", docs)

# Build prompt
prompt = f"""
Analyze the following streaming messages:

{chr(10).join(docs)}

- Infer schema
- Detect data patterns
- Identify anomalies
- Suggest schema field names or types
"""

print("Sending prompt to LLaMA...")
try:
    response = requests.post("http://ollama:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })
    summary = response.json()["response"]
except Exception as e:
    print("LLM call failed:", e)
    exit(1)

print("LLM response received.")
print("Summary:", summary)

# Insert result into DB
try:
    cursor.execute(
        "INSERT INTO rag_insights (input_sample, llm_summary, topic, tags) VALUES (%s, %s, %s, %s)",
        (json.dumps(docs), summary, "raw-stream", ['inferred']),
    )
    conn.commit()
    print("Stored LLM output in PostgreSQL.")
except Exception as e:
    print("Postgres insert failed:", e)
    exit(1)

