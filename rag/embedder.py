from chromadb import Client
from sentence_transformers import SentenceTransformer
import json

client = Client()
collection = client.get_or_create_collection(name="stream_samples")
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_and_store(json_docs):
    texts = [json.dumps(doc) for doc in json_docs]
    embeddings = model.encode(texts).tolist()
    collection.add(documents=texts, embeddings=embeddings, ids=[str(i) for i in range(len(texts))])
