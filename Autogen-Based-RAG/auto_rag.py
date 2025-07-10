import os
import json
import logging
import pandas as pd
from autogen import AssistantAgent, UserProxyAgent
from sentence_transformers import SentenceTransformer
from opensearchpy import OpenSearch
from google.generativeai import GenerativeModel
from diskcache import Cache
import hashlib

CACHE_PATH = "gemini_cache.json"
if not os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "w") as f:
        json.dump({}, f)

def load_cache():
    with open(CACHE_PATH, "r") as f:
        return json.load(f)

def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)

def get_cache_key(prompt: str) -> str:
    return hashlib.sha256(prompt.encode()).hexdigest()

def cache_gemini_response(prompt: str, generate_func):
    cache = load_cache()
    key = get_cache_key(prompt)

    if key in cache:
        print("⚡ Using cached response for Gemini.")
        return cache[key]
    else:
        print("🌐 Sending request to Gemini API...")
        response = generate_func(prompt)
        cache[key] = response
        save_cache(cache)
        return response


# === CONFIG ===
GEMINI_API_KEY = "AIzaSyCB4IRmsJurOemf77HxmUC2GZ7J49se7PY"  # <-- Replace this
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
OPENSEARCH_INDEX = "agentic-rag-index"
cache = Cache("cache_dir")
logging.basicConfig(level=logging.INFO)

# === OPENSEARCH SETUP ===
client = OpenSearch(hosts=[{"host": "localhost", "port": 9200}], http_compress=True)

if client.indices.exists(index=OPENSEARCH_INDEX):
    client.indices.delete(index=OPENSEARCH_INDEX)

client.indices.create(index=OPENSEARCH_INDEX, body={
    "settings": {
        "index": {
            "knn": True,
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "vector": {
                "type": "knn_vector",
                "dimension": 384,
                "method": {
                    "name": "hnsw",
                    "engine": "faiss",          
                    "space_type": "l2"           
                }
            }
        }
    }
})


# === GEMINI CHAT WRAPPER ===
def gemini_chat(prompt: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    def call_model(p):
        response = model.generate_content(p)
        return response.text

    return cache_gemini_response(prompt, call_model)


# === FUNCTIONAL AGENT TASKS ===

def extract_unstructured(path="data/products.csv"):
    df = pd.read_csv(path)
    return df["description"].dropna().tolist()

def embed_and_store(texts):
    vectors = EMBED_MODEL.encode(texts)
    for text, vector in zip(texts, vectors):
        client.index(index=OPENSEARCH_INDEX, body={
            "text": text,
            "vector": vector.tolist()
        })

def search_opensearch(query, k=5):
    vector = EMBED_MODEL.encode([query])[0].tolist()
    response = client.search(index=OPENSEARCH_INDEX, body={
        "size": k,
        "query": {
            "knn": {
                "vector": {
                    "vector": vector,
                    "k": k
                }
            }
        }
    })
    return [hit["_source"]["text"] for hit in response["hits"]["hits"]]

# === GEMINI CONFIG FOR AGENTS ===
config = {
    "model": "gemini-1.5-flash",
    "api_type": "google",
    "api_key": GEMINI_API_KEY,
    "base_url": "https://generativelanguage.googleapis.com/v1beta/models"
}
llm_config = {"config_list": config}

# === AGENTS ===
user_proxy = UserProxyAgent(name="UserProxy", human_input_mode="NEVER", code_execution_config=False)

extractor_agent = AssistantAgent(
    name="ExtractorAgent",
    llm_config=llm_config,
    system_message="Extract unstructured text data from the provided CSV file."
)

embedder_agent = AssistantAgent(
    name="EmbedderAgent",
    llm_config=llm_config,
    system_message="Embed the given list of text and store embeddings into OpenSearch."
)

answer_agent = AssistantAgent(
    name="AnswerAgent",
    llm_config=llm_config,
    system_message="Use the retrieved context to generate a detailed answer to the user's query."
)

# === RAG EXECUTION ===
def run_agentic_rag():
    logging.info("🔍 Step 1: Extracting data...")
    extracted = extract_unstructured("data/products.csv")

    logging.info("🔐 Step 2: Embedding and indexing...")
    embed_and_store(extracted)

    user_query = input("❓ Enter your query: ")
    logging.info("🔎 Step 3: Searching in vector DB...")
    results = search_opensearch(user_query)

    context = "\n".join(results)
    final_prompt = f"""You are a helpful assistant. Use the following context to answer the question.

Context:
{context}

Question:
{user_query}

Answer:"""

    logging.info("🧠 Step 4: Answering with Gemini...")
    answer = gemini_chat(final_prompt)
    print("\n✅ Final Answer:\n", answer)

# === MAIN ===
if __name__ == "__main__":
    run_agentic_rag()
