import os
import uuid
import json
import pandas as pd
import logging
import requests
from typing import List, Dict, Union
from sqlalchemy import create_engine
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch

# Configurations
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
LM_STUDIO_MODEL ="mistral-7b-instruct-v0.1"  # change if using another model
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "http://localhost:9200")
OPENSEARCH_INDEX = "rag-lmstudio-index"
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# OpenSearch client
os_client = OpenSearch(hosts=[OPENSEARCH_HOST])

# ---------------- Agent: Extractor ----------------

def extract_unstructured_from_csv(csv_path: str, text_column: str) -> List[str]:
    df = pd.read_csv(csv_path)
    return df[text_column].dropna().astype(str).tolist()

def extract_unstructured_from_sqlite(db_path: str, table: str, text_column: str) -> List[str]:
    engine = create_engine(f"sqlite:///{db_path}")
    df = pd.read_sql(f"SELECT {text_column} FROM {table}", engine)
    return df[text_column].dropna().astype(str).tolist()

# ---------------- Agent: Chunker ----------------

def chunk_texts(texts: List[str], max_words: int = 200) -> List[str]:
    chunks = []
    for text in texts:
        words = text.split()
        for i in range(0, len(words), max_words):
            chunks.append(" ".join(words[i:i+max_words]))
    return chunks

# ---------------- Agent: Embedder ----------------

def embed_chunks(chunks: List[str]) -> List[Dict]:
    embedded_docs = []
    for chunk in chunks:
        embedding = EMBEDDING_MODEL.encode(chunk).tolist()
        embedded_docs.append({
            "id": str(uuid.uuid4()),
            "text": chunk,
            "embedding": embedding
        })
    return embedded_docs

# ---------------- Agent: Indexer ----------------

def create_index_if_needed(index_name: str, dim: int = 384):
    if not os_client.indices.exists(index=index_name):
        os_client.indices.create(index=index_name, body={
            "settings": {
                "index": {"number_of_shards": 1, "number_of_replicas": 0, "knn": True}
            },
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "embedding": {
                        "type": "knn_vector",
                        "dimension": dim,
                        "method": {"name": "hnsw", "engine": "faiss"}
                    }
                }
            }
        })

def index_documents(index_name: str, docs: List[Dict]):
    for doc in docs:
        os_client.index(index=index_name, id=doc["id"], body={
            "text": doc["text"],
            "embedding": doc["embedding"]
        })
    os_client.indices.refresh(index=index_name)

# ---------------- Agent: Retriever ----------------

def retrieve_similar_documents(query: str, top_k: int = 3) -> List[str]:
    embedding = EMBEDDING_MODEL.encode(query).tolist()
    search_query = {
        "size": top_k,
        "query": {
            "knn": {
                "embedding": {
                    "vector": embedding,
                    "k": top_k
                }
            }
        }
    }
    response = os_client.search(index=OPENSEARCH_INDEX, body=search_query)
    return [hit["_source"]["text"] for hit in response["hits"]["hits"]]

# ---------------- Agent: Answer Generator ----------------

def generate_answer_lmstudio(contexts: List[str], query: str) -> str:
    prompt = f"""You are a helpful assistant. Use the context below to answer the question.

Context:
{chr(10).join(contexts)}

Question: {query}
Answer:"""

    payload = {
        "model": LM_STUDIO_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 300
    }
    response = requests.post(LM_STUDIO_URL, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# ---------------- Main Orchestration ----------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # ---- Step 1: Extract ----
    data_source = "csv"  # or 'sqlite'
    if data_source == "csv":
        texts = extract_unstructured_from_csv("data/products.csv", text_column="description")
    else:
        texts = extract_unstructured_from_sqlite("data/products.db", table="inventory", text_column="description")

    # ---- Step 2: Chunk ----
    chunks = chunk_texts(texts)
    logging.info(f"Chunked into {len(chunks)} segments")

    # ---- Step 3: Embed ----
    embedded_docs = embed_chunks(chunks)

    # ---- Step 4: Index ----
    create_index_if_needed(OPENSEARCH_INDEX)
    index_documents(OPENSEARCH_INDEX, embedded_docs)
    logging.info("Documents embedded & indexed")

    # ---- Step 5: Query ----
    user_query = "Which will be the most selling products and which will be the least selling ones?"
    retrieved = retrieve_similar_documents(user_query)
    logging.info("Retrieved relevant contexts")

    # ---- Step 6: Generate ----
    answer = generate_answer_lmstudio(retrieved, user_query)
    print("\nAnswer:\n", answer)
