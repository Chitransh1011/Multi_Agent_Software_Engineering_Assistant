from langchain_text_splitters import CharacterTextSplitter

def split_documents(documents):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=100,
        chunk_overlap=0,
    )

    return splitter.split_documents(documents)