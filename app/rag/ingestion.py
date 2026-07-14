from app.rag.loader import load_documents
from app.rag.splitter import split_documents
from app.rag.embeddings import embedding_model
from app.rag.vector_store import build_vector_store
from pathlib import Path
from langchain_community.vectorstores import FAISS
VECTOR_STORE_PATH = "vector_store"

def ingest_documents(path:str):
    if Path(VECTOR_STORE_PATH).exists():
        print("Loading existing FAISS index...")

        return FAISS.load_local(
            VECTOR_STORE_PATH,
            embedding_model,
            allow_dangerous_deserialization=True,
        )


    loader = load_documents(path=path)

    chunks = split_documents(loader)

    vector_store = build_vector_store(chunks=chunks,embedding_model=embedding_model)

    vector_store.save_local(VECTOR_STORE_PATH)
    
    return vector_store







