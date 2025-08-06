# 🩺 Medical Document QA Chatbot (RAG with PubMedBERT + Gemini)

A powerful Question Answering chatbot for medical PDFs (e.g. **IMCI Chart Booklet**, **Pocket Book of Hospital Care for Children**) built using a **Retrieval-Augmented Generation (RAG)** pipeline with:

- 🧠 **PubMedBERT** for domain-specific embeddings  
- ⚡ **Gemini Flash** for fast, cost-efficient LLM responses  
- 🗂️ **FAISS** for scalable similarity search  
- 🌐 **FastAPI** backend to serve as an inference API  
- 🧾 **Structured document parsing** (tables, headings, charts)  
- 💬 **Conversational memory** with intelligent follow-up tracking  

---

## 🔧 Features

- ✅ Chunk-by-item parsing with full metadata (page, section, file)
- ✅ Table-aware embedding using markdown standardization
- ✅ Follow-up detection using Gemini (YES/NO based)
- ✅ Dynamic query rewriting for context-aware answers
- ✅ Gemini Flash-powered answers with exact citations
- ✅ Incremental document ingestion without recomputing old embeddings
- ✅ FAISS-powered retrieval for top-K relevant chunks
- ✅ Deployable with FastAPI (`/ask` endpoint)

---

## 🗺️ Architecture Overview

```text
User Query
   │
   ▼
/ask (FastAPI)
   │
   ▼
Conversational Pipeline
   ├── Check for follow-up (Gemini)
   ├── Rewrite query if needed
   ├── Retrieve top-K chunks (PubMedBERT + FAISS)
   ├── Generate answer (Gemini Flash)
   └── Return final answer with citation

Data Pipeline
   ├── Parse PDFs with OCR + StructureV3
   ├── Chunk JSON into [value + md] pairs
   ├── Store chunks with metadata
   ├── Create 768-dim embeddings via PubMedBERT
   └── Index all vectors in FAISS
