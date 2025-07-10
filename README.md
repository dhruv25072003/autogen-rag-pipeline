# autogen-rag-pipeline
# 🧠 Agentic RAG Pipeline

A fully local, production-grade **Retrieval-Augmented Generation (RAG)** system using **AutoGen agents**, **OpenSearch** vector search, and **local LLMs** (e.g., Mistral via LM Studio or Gemini API). This project showcases how multiple intelligent agents can collaborate to extract, chunk, embed, index, and answer over **unstructured data inside structured sources** (like CSV, Excel, SQL).

---

## 🚀 Features

- 🤖 **Multi-Agent Workflow** using AutoGen
- 📄 Extracts embedded unstructured text from structured databases
- 🔍 Semantic search over embeddings using **OpenSearch**
- 🧠 Local embedding via **SentenceTransformers**
- 🗂️ End-to-end chunking, indexing, and retrieval
- 💬 Query answering with **local or API LLMs** (Gemini / Mistral via LM Studio)
- 💾 Caching + fallback for cost-efficiency
- 📊 (Optional) Streamlit UI for demo interface

---

## 🛠️ Architecture


All agents communicate through **AutoGen group chat** using structured message passing.

---

## 🧱 Tech Stack

| Component        | Stack                                 |
|------------------|----------------------------------------|
| RAG Engine       | Python + AutoGen                       |
| Vector Store     | OpenSearch (local)                     |
| Embedding Model  | `all-MiniLM-L6-v2` (SentenceTransformers) |
| LLM              | Mistral via LM Studio / Gemini Pro API |
| Interface (opt)  | Streamlit (for end-to-end demo)        |


---

🧪 How to Run the Project
🔧 1. Clone the repository
git clone https://github.com/yourusername/agentic-rag-pipeline.git
cd agentic-rag-pipeline

Replace yourusername with your actual GitHub username.

📦 2. Set up a Python environment
python -m venv venv
source venv/bin/activate       # On Linux/Mac
venv\Scripts\activate          # On Windows

📥 3. Install dependencies
pip install -r requirements.txt


🔍 4. Start OpenSearch locally
docker run -d -p 9200:9200 -e "discovery.type=single-node" -e "plugins.security.disabled=true" opensearchproject/opensearch:latest


🚀 5. Run the agentic RAG pipeline
python (whatever is your file name).py
(Make sure the directory in which file is opened is selected in the terminal using cd)


🌐 6. (Optional) Run the Streamlit UI
streamlit run app/streamlit_ui.py


💡 7. Example Query
After everything is set up, you can:

Upload a CSV/Excel file with embedded text

Ask a question like:

“Summarize customer pain points in the past quarter”
“What do users complain about most?”

Your agentic system will:

Extract unstructured data

Embed it

Search relevant chunks via OpenSearch

Answer the query using a local or API LLM





