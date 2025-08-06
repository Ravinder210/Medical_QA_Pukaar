# rag_incremental_indexer.py

import json
import pickle
import faiss
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

class RAGIndexer:
    def __init__(self, 
                 faiss_index_path="data/faiss_index.index", 
                 texts_path="data/texts.pkl", 
                 metadatas_path="data/metadatas.pkl", 
                 embedding_model_name="NeuML/pubmedbert-base-embeddings",
                 gemini_model_name="gemini-2.5-flash"):

        self.faiss_index_path = faiss_index_path
        self.texts_path = texts_path
        self.metadatas_path = metadatas_path
        self.gemini_model_name = gemini_model_name

        # Load embedding model
        self.model = SentenceTransformer(embedding_model_name)

        # Try to load existing index and data
        try:
            self.index = faiss.read_index(self.faiss_index_path)
            with open(self.texts_path, "rb") as f:
                self.texts = pickle.load(f)
            with open(self.metadatas_path, "rb") as f:
                self.metadatas = pickle.load(f)
            length = len(self.metadatas)
            print(f"✅ Loaded existing index and data {len(self.metadatas)}")
        except:
            self.index = None
            self.texts = []
            self.metadatas = []
            print("⚠️ Starting with empty index.")

    def update_with_jsonl(self, jsonl_path):
        # Load new JSONL file
        new_texts = []
        new_metas = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                new_texts.append(obj["content"])
                new_metas.append(obj["metadata"])

        # Embed new content
        new_embeddings = self.model.encode(new_texts, convert_to_numpy=True)

        # Initialize index if needed
        if self.index is None:
            dim = new_embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dim)

        # Add to index and local lists
        self.index.add(new_embeddings)
        self.texts.extend(new_texts)
        self.metadatas.extend(new_metas)

        # Save everything back
        faiss.write_index(self.index, self.faiss_index_path)
        with open(self.texts_path, "wb") as f:
            pickle.dump(self.texts, f)
        with open(self.metadatas_path, "wb") as f:
            pickle.dump(self.metadatas, f)

        print(f"✅ Added {len(new_texts)} chunks from {jsonl_path}")

    def search(self, query, top_k=10):
        # Encode query
        query_vec = self.model.encode([query], convert_to_numpy=True)

        # Search
        D, I = self.index.search(query_vec, top_k)

        return [(self.texts[i], self.metadatas[i], D[0][rank]) for rank, i in enumerate(I[0])]

    def generate_answer(self, query, top_k=3, api_key=None):
        if api_key:
            genai.configure(api_key=api_key)

        model = genai.GenerativeModel(self.gemini_model_name)
        results = self.search(query, top_k=top_k)

        context_blocks = []
        for text, meta, score in results:
            context_blocks.append(
                f"Source: {meta.get('source', '')} Page: {meta['page']}, Section: {meta.get('section', '')}\n{text.strip()}"
            )

        system_prompt = (
            "You are a helpful clinical assistant. Use only the provided context to answer.\n"
            "Always cite the Section and page number from the metadata."
        )

        final_prompt = f"{system_prompt}\n\nUser Query:\n{query}\n\nContext:\n" + "\n\n".join(context_blocks)

        response = model.generate_content(final_prompt)
        return response.text


