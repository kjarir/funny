# utils/pdf_reader.py
from langchain_community.document_loaders import PyMuPDFLoader
import os

def load_pdfs(pdf_paths):
    docs = []
    for path in pdf_paths:
        # Convert to absolute path if it's not already
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            raise ValueError(f"PDF file not found: {abs_path}")
        loader = PyMuPDFLoader(abs_path)
        docs.extend(loader.load())
    return docs
