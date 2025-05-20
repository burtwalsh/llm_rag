from chromadb import Client
from sentence_transformers import SentenceTransformer
import json
import requests

client = Client()
collection = client.get_or_create_collection("stream_samples")
model = SentenceTransformer("all-MiniLM-L6-v2")

def infer_with_ollama(prompt: str):
    response = requests.post("http://ollama:11434/api/generate", json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

def get_recent_samples_and_insights():
    results = collection.peek(limit=5)
    samples = results["documents"]

    prompt = f"""
Analyze the following streaming messages:

{chr(10).join(samples)}

- Infer schema
- Detect data patterns
- Identify any anomalies
- Suggest schema field names or types
"""
    summary = infer_with_ollama(prompt)
    return samples, summary
