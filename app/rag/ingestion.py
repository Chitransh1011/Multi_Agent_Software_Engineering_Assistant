from app.rag.loader import load_documents
from app.rag.splitter import split_documents
from app.rag.embeddings import embedding_model
from app.rag.vector_store import build_vector_store

def ingest_documents(path:str):

    loader = load_documents(path=path)

    chunks = split_documents(loader)

    vector_store = build_vector_store(chunks=chunks,embedding_model=embedding_model)
    
    return vector_store







