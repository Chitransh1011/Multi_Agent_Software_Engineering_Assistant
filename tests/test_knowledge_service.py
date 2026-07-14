from app.services.knowledge_service import KnowledgeService


class FakeDocument:

    def __init__(self, content):
        self.page_content = content


class FakeRetriever:

    def invoke(self, query):
        return [
            FakeDocument("Git is a version control system."),
            FakeDocument("Use git init to create a repository."),
        ]


def test_retrieve_context():

    service = KnowledgeService(
        retriever=FakeRetriever(),
    )

    context = service.retrieve(
        "How to create git repo?"
    )

    assert "Git is a version control system." in context

    assert "git init" in context