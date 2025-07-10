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

## 📂 Folder Structure


---

## 🧪 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/agentic-rag-pipeline.git
cd agentic-rag-pipeline


2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Start OpenSearch locally
bash
Copy
Edit
./start_opensearch.sh   # or use Docker
4. Run the pipeline
bash
Copy
Edit
python app/rag_runner.py
5. (Optional) Run the UI
bash
Copy
Edit
streamlit run app/streamlit_ui.py
🧠 Use Cases
Customer feedback summarization from CRM exports

Legal clause extraction and retrieval

Financial report Q&A

HR or Resume parsing & intelligent querying

💡 Coming Soon
Agent memory + intermediate state tracking

Automatic logging + recovery from agent failures

Hybrid cloud/local LLM fallback setup

Dashboard to monitor agent performance

👤 Author
DSK (Dhruv S Kumar)
Final year BTech student | AI Engineer in the making | 2.5 years gym discipline meets GenAI obsession 💪🧠

🏁 Goal
To ship a real-world capable agentic GenAI system by end of 2025 — and prove that even with no prior income, no Ivy League degree, and no connections, discipline + vision = undeniable results.
