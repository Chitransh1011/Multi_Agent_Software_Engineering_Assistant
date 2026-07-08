


class KnowledgeService:

    def __init__(self,retriever):
        self.retriever = retriever

    def retrieve(self, query: str) -> str:

        docs = self.retriever.invoke(query)

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        return context