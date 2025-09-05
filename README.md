# 🧠 autogen-rag-pipeline

> **Agentic RAG: The next-gen, production-ready, fully local Retrieval-Augmented Generation pipeline—built with multi-agent AutoGen orchestration, OpenSearch semantic search, and blazing-fast local LLMs.**

---

## 🚀 What is This?

A future-proof RAG stack that *truly thinks for itself*—through collaborating generative agents, on your infrastructure, using your data.

**Demo:**
- ✅ Extract unstructured text from structured sources (CSV, Excel, SQL)
- ✅ Dynamically chunk, embed, index and semantically search with OpenSearch
- ✅ Answer queries with *local* open-source LLMs (Mistral via LM Studio, Gemini API) or your favorite API model
- ✅ All orchestrated by AutoGen agents talking in structured chat!

---

## 🤖 How It Works (Agentic Flow)

1. **Ingest:** Upload anything—Excel/CSV, SQL with hidden text blobs...
2. **Extract:** Multi-agent chat system identifies and extracts “meaningful” unstructured data scattered anywhere.
3. **Chunk & Embed:** Agents split data into optimal, context-aware chunks. Vectorized locally using `all-MiniLM-L6-v2` or your favorite SentenceTransformer.
4. **Index:** All chunks are indexed in a local OpenSearch vector DB.
5. **Query:** Any question is “multi-hop” handled by agents:
    - Retriever agent finds relevant context chunks (semantic search)
    - LLM agent generates answers using your choice of local LLM/APIs (Gemini/Mistral)
    - Everything is logged, cached, and optionally visualized.

---

## 🔑 Features at a Glance

- 🤝 **Multi-agent orchestration:** True distributed agent workflows powered by [AutoGen](https://github.com/microsoft/autogen)
- 🗃️ **Universal data extraction:** Handles embedded text in structured data—no file format left behind!
- ⚡ **Semantic vector search:** Fast, scalable retrieval via OpenSearch
- 🏠 **100% local-first:** Full privacy, no vendor lock-in (bring your own LLM via LM Studio or run with Gemini API)
- 🧠 **Embeddings:** SOTA SentenceTransformers (default: `all-MiniLM-L6-v2`)
- 🌐 **Real-time interface:** (Optional) Streamlit UI for demo/playground
- 💸 **Caching, fallback, cost control:** Designed for *production*, not just proof-of-concept.

---

## 🛠️ Quickstart (Local Usage)

```
# 1. Clone this repo
git clone https://github.com/dhruv25072003/autogen-rag-pipeline.git
cd autogen-rag-pipeline

# 2. (Recommended) Create a virtualenv
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start OpenSearch (local, via Docker)
docker run -d -p 9200:9200 -e "discovery.type=single-node" -e "plugins.security.disabled=true" opensearchproject/opensearch:latest

# 5. Run the pipeline!
python agentic_rag_pipeline.py
# (Replace with your main file)

# 6. (Optional) Launch Streamlit UI 💻
streamlit run app/streamlit_ui.py
```

---

## 🧪 Example Query

After setup:
- Upload a data file (CSV/Excel, etc.)
- Ask:
    - _“Summarize all customer pain points since April”_
    - _“What’s our most frequent support theme by ticket?”_
    - _“What did reviewers complain about in Q2?”_

The pipeline:
- Will extract, chunk, embed, semantic-search, and LLM-answer using your local/private stack

---

## 🧱 Architecture Overview

```
┌─────────────┐     ┌───────────┐         ┌────────────┐    ┌──────────────┐
│  CSV/Excel  │     │  AutoGen  │         │ SentenceT. │    │ OpenSearch   │
│  SQL Table  │─►──►│  Agents   │─Chunk─► │ Embeddings │─►──│  Vector DB   │
└─────────────┘     └───────────┘         └────────────┘    └──────────────┘
       │                       │                                  ▲
       │<──────<──<──User Q────┘                                  │
       ▼                                                          │
   LLM (Local/API) <--- Multi-agent context  <--------------------┘
```

All actors communicate by structured group chat. Easily plug in your own LLM & agent logic.

---

## 📦 Tech Stack

| Component         | Technology                             |
|-------------------|----------------------------------------|
| RAG Engine        | Python + [AutoGen](https://github.com/microsoft/autogen)      |
| Vector DB         | [OpenSearch (local)](https://opensearch.org/)                 |
| Embeddings        | SentenceTransformers (`all-MiniLM-L6-v2`)          |
| LLM               | Mistral (LM Studio), Gemini API, or any local API |
| UI (optional)     | Streamlit                              |

---

## 🌈 Why Use This?

- **True "agentic" AI ops:** Showcase, prototype, or deploy cutting-edge agent workflows
- **Full privacy:** All local if you want—no data leaves your machine!
- **Plug & play:** Swap LLMs, embedding models, or add new agent types without changing data ops code
- **Built for modern MLOps workflows**

---

## ⭐ Inspiration & Credits

- [AutoGen by Microsoft](https://github.com/microsoft/autogen)
- [LM Studio by lmstudio.ai](https://lmstudio.ai/)
- [SentenceTransformers](https://www.sbert.net/)
- [OpenSearch](https://opensearch.org/)

---

## 📝 License

MIT

---

**Contribute | Star | Try it on your local data → Let’s push agentic retrieval to the next level! 🚀**

