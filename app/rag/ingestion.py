from app.rag.loader import load_documents
from app.rag.splitter import split_documents
from app.rag.embeddings import embedding_model
from app.rag.vector_store import build_vector_store


def ingest_documents(path: str):
    vector_store = build_vector_store(embedding_model)

    # Reuse an already populated collection.
    if vector_store.get(limit=1)["ids"]:
        return vector_store

    documents = load_documents(path=path)
    chunks = split_documents(documents)

    if chunks:
        vector_store.add_documents(chunks)

    return vector_store