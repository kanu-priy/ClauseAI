<div align="center">

# 🧾 ClauseAI

### Multi-Agent Contract Intelligence Platform

Parallel AI agents that read, analyze, and answer questions about legal contracts — with citations.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square)
![Pinecone](https://img.shields.io/badge/Pinecone-000000?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini%202.5%20Flash-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

[Overview](#-overview) · [Features](#-features) · [Architecture](#-architecture) · [Setup](#-setup) · [Usage](#-usage) · [Roadmap](#-roadmap)

</div>

---

## 📖 Overview

ClauseAI is a multi-agent system that automates contract review. Instead of a single model reading a document linearly from top to bottom, ClauseAI dispatches specialized agents in parallel to extract risks, summarize clauses, and answer natural-language questions about the contract — with every answer backed by a citation to the exact source text.

Built during the **Infosys Springboard Virtual Internship 6.0**.

## ✨ Features

- 🤖 **Parallel agent execution** — specialized agents (risk detection, summarization, Q&A) run concurrently via LangGraph instead of sequentially, reducing overall review time
- ⚠️ **Risk dashboard** — flags risky or unusual clauses (liability, termination, indemnity, penalty, etc.) with severity indicators
- 💬 **Citation-based Q&A** — ask questions about the contract in plain English; every answer links back to the exact clause it was derived from
- 📄 **PDF export** — generate a shareable summary report of the analysis
- 🔍 **Semantic search** — contract text is embedded and indexed in Pinecone for fast, meaning-based retrieval rather than plain keyword search

## 🏗️ Architecture
                     ┌───────────────────────┐
                     │     Contract Upload     │
                     │      (PDF / DOCX)       │
                     └───────────┬─────────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │   Text Extraction &     │
                     │      Chunking           │
                     └───────────┬─────────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │  Embedding Generation   │
                     │   → Pinecone Vector DB  │
                     └───────────┬─────────────┘
                                 │
                                 ▼
                ┌────────────────────────────────┐
                │      LangGraph Orchestrator      │
                │  (routes to parallel agents)     │
                └───┬────────────┬────────────┬───┘
                    ▼            ▼            ▼
             ┌───────────┐ ┌───────────┐ ┌───────────┐
             │   Risk     │ │  Summary   │ │    Q&A     │
             │  Analysis  │ │   Agent    │ │   Agent    │
             │   Agent    │ │            │ │            │
             └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
                   │              │              │
                   └──────────────┼──────────────┘
                                  ▼
                     ┌───────────────────────┐
                     │   Gemini 2.5 Flash      │
                     │   (LLM inference for     │
                     │    all agent calls)      │
                     └───────────┬─────────────┘
                                 │
                                 ▼
                     ┌───────────────────────┐
                     │     Streamlit UI        │
                     │  (dashboard, chat,       │
                     │   PDF export)            │
                     └───────────────────────┘

Each agent operates on a shared LangGraph state object. The orchestrator fans out to the risk, summary, and Q&A agents concurrently, waits for all branches to complete, then merges their outputs before rendering the dashboard.

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | LangGraph, LangChain |
| LLM | Gemini 2.5 Flash |
| Vector Store | Pinecone |
| Frontend | Streamlit |
| Language | Python |

*(adjust to match your actual folder layout)*

## 🚀 Setup

### Prerequisites
- Python 3.10+
- A Gemini API key
- A Pinecone API key

### Installation

```bash
# Clone the repo
git clone https://github.com/kanu-priy/ClauseAI.git
cd ClauseAI

# Create a virtual environment
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
```

### Run the app

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

## 🧑‍💻 Usage

1. Upload a contract (PDF/DOCX) via the sidebar
2. The document is chunked, embedded, and indexed in Pinecone
3. Risk, summary, and Q&A agents run in parallel over the indexed content
4. View flagged clauses in the risk dashboard
5. Ask questions in the Q&A panel — answers include citations to the source clause
6. Export a summary report as PDF

## 🗺️ Roadmap

- [ ] Multi-document comparison (compare two contract versions side by side)
- [ ] OCR support for scanned/image-based PDFs
- [ ] Clause negotiation suggestions
- [ ] Multi-language contract support
- [ ] Deploy a hosted demo

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/kanu-priy/ClauseAI/issues).

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Kanupriya**
- GitHub: [@kanu-priy](https://github.com/kanu-priy)
- LinkedIn: [Kanupriya Varshney](https://linkedin.com/in/kanupriya-varshney-27445427b)

---

<div align="center">

⭐ If you found this project useful, consider giving it a star!

</div>
