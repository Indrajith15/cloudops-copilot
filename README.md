
# ☁️ CloudOps Copilot

**An Agentic RAG-powered cloud troubleshooting assistant built with LangChain, LangGraph, Gemini and ChromaDB.**

CloudOps Copilot helps developers troubleshoot cloud infrastructure issues by retrieving relevant technical documentation, evaluating retrieved information and generating context-grounded troubleshooting guidance.

## 🚀 Live Demo

**Try CloudOps Copilot:** https://cloudops-copilot.streamlit.app/

Ask cloud troubleshooting questions and get AI-generated answers grounded in documentation, with retrieved sources.

<img width="1905" height="912" alt="Screenshot 2026-11-06 133759" src="https://github.com/user-attachments/assets/ba13bb7e-2921-48df-ae63-4c6870c5fe87" />



## ✨ Features

- **Document Ingestion:** Load, split and process cloud troubleshooting documentation.
- **Vector Search:** Generate embeddings using Gemini and store them in ChromaDB.
- **Advanced Retrieval:** Metadata filtering, similarity search and configurable Top-K retrieval.
- **Query Rewriting:** Improve vague troubleshooting queries.
- **Agentic RAG:** Use LangGraph to retrieve, grade and retry document retrieval.
- **Fallback Handling:** Handle questions when sufficient documentation is unavailable.
- **Faithfulness Evaluation:** Evaluate whether generated answers are supported by retrieved context.
- **Source Tracking:** Display retrieved document chunks and their source metadata.
- **Interactive UI:** Chat interface built with Streamlit.

## 🏗️ Architecture

```text
User Question
     |
     v
Query Rewriting
     |
     v
ChromaDB Retriever
     |
     v
Document Grading
     |
     +------ Relevant? ------+
     |                       |
    Yes                      No
     |                       |
     v                       v
Generate Answer         Rewrite Query
     |                       |
     v                       v
Faithfulness Check      Retry Retrieval
     |                       |
     v                       v
Streamlit UI            Fallback
     |
     v
Display Answer + Sources
```

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | RAG pipeline and LCEL |
| LangGraph | Agentic workflow orchestration |
| Gemini | Embeddings, query rewriting and answer generation |
| ChromaDB | Vector database |
| Streamlit | User interface |

## 📁 Project Structure

```text
cloudops-copilot/
├── agent/
│   ├── state.py
│   ├── nodes.py
│   └── graph.py
├── chains/
│   ├── prompts.py
│   └── rag_chain.py
├── data/
│   └── documents/
├── evaluation/
│   └── test_questions.json
├── ingestion/
│   ├── loader.py
│   ├── chunker.py
│   └── embeddings.py
├── retrieval/
│   ├── vector_store.py
│   └── retriever.py
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd cloudops-copilot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

Never commit your actual API key.

### 5. Run the application

```bash
streamlit run app.py
```

## 🧠 Agentic Workflow

CloudOps Copilot uses LangGraph to orchestrate its troubleshooting workflow:

1. Receive the user's question.
2. Retrieve relevant documentation.
3. Grade retrieved documents for relevance.
4. Rewrite the query if documents are insufficiently relevant.
5. Retry retrieval within a configured limit.
6. Generate an answer using retrieved context.
7. Evaluate answer faithfulness.
8. Return the answer and source documents.

## 📚 Current Documentation Coverage

The initial knowledge base contains a curated Google Cloud Run troubleshooting guide covering:

- HTTP 503 errors
- Container startup failures
- Memory issues

The knowledge base can be expanded with additional cloud documentation.

## 🔮 Future Improvements

- Support additional GCP, AWS and Azure services.
- Expand the troubleshooting knowledge base.
- Improve retrieval and evaluation metrics.
- Add deployment and monitoring capabilities.

## 👨‍💻 Author

**Indrajith Nair**

Built as a hands-on project to explore Retrieval-Augmented Generation, Agentic AI and cloud troubleshooting automation.
