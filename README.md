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
bash
Copy
Edit
git clone https://github.com/yourusername/agentic-rag-pipeline.git
cd agentic-rag-pipeline
Replace yourusername with your actual GitHub username.

📦 2. Set up a Python environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate       # On Linux/Mac
venv\Scripts\activate          # On Windows
📥 3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔍 4. Start OpenSearch locally
If you’re using Docker (recommended):

bash
Copy
Edit
docker run -d -p 9200:9200 -e "discovery.type=single-node" -e "plugins.security.disabled=true" opensearchproject/opensearch:latest
Or use your local OpenSearch setup if already configured.

🚀 5. Run the agentic RAG pipeline
bash
Copy
Edit
python app/rag_runner.py
This script will orchestrate your AutoGen agents to extract, embed, index, retrieve, and answer using local LLMs or Gemini API.

🌐 6. (Optional) Run the Streamlit UI
bash
Copy
Edit
streamlit run app/streamlit_ui.py
This launches an interactive web app for document upload and query answering using your pipeline.

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





