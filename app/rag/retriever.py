from app.rag.ingestion import ingest_documents

def get_retriever(path:str):

    vector_store = ingest_documents(path=path)
    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )