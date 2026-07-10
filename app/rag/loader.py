from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
def load_documents(path: str):
    print("Loading:", Path(path).resolve())
    loader = PyPDFLoader(path)
    return loader.load()