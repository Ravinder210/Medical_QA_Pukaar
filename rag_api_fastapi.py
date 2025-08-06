from fastapi import FastAPI
from pydantic import BaseModel
from rag_incremental_indexer import RAGIndexer

import uvicorn




indexer = RAGIndexer(
    faiss_index_path="data/faiss_index.index",
    texts_path="data/texts.pkl",
    metadatas_path="data/metadatas.pkl"
)

# Define FastAPI app
app = FastAPI()

class QARequest(BaseModel):
    query: str
    top_k: int = 10
    gemini_api_key: str

@app.post("/ask")
async def ask_question(request: QARequest):
    try:
        answer = indexer.generate_answer(
            query=request.query,
            top_k=request.top_k,
            api_key=request.gemini_api_key
        )
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "Medical QA RAG API is running!"}