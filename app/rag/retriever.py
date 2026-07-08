from app.rag.vector_store import vector_store

def get_retriever():
    return vector_store.as_retriever(
        search_kwargs={"k": 3}
    )