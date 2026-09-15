from pathlib import Path
from langchain_chroma import Chroma

VECTOR_STORE_PATH = str(
    Path(__file__).resolve().parents[2] / "chroma_store"
)


def build_vector_store(embedding_model):
    return Chroma(
        collection_name="engineering_knowledge",
        embedding_function=embedding_model,
        persist_directory=VECTOR_STORE_PATH,
    )