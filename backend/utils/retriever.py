# utils/retriever.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_index(documents):
    texts = [doc.page_content for doc in documents]
    embeddings = model.encode(texts)
    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(np.array(embeddings))
    return index, texts
