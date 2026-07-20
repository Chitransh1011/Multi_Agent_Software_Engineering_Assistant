from uuid import uuid4

from app.db.models.artifact import Artifact
from app.db.models.conversation import Conversation
from app.db.repositories.artifact_repository import ArtifactRepository


def create_conversation():
    return Conversation(
        request_id=uuid4(),
        user_query="Test Conversation",
    )


def create_artifact(conversation_id, filename="main.py"):
    return Artifact(
        conversation_id=conversation_id,
        filename=filename,
        artifact_type="python",
        description="Test artifact",
        content="print('Hello World')",
    )


def test_add_and_get_artifact(db_session):
    conversation = create_conversation()
    db_session.add(conversation)
    db_session.commit()

    repo = ArtifactRepository(db_session)

    artifact = create_artifact(conversation.id)

    repo.add(artifact)
    db_session.commit()

    fetched = repo.get(artifact.id)

    assert fetched is not None
    assert fetched.id == artifact.id
    assert fetched.filename == "main.py"


def test_get_non_existing_artifact(db_session):
    repo = ArtifactRepository(db_session)

    artifact = repo.get(uuid4())

    assert artifact is None

def test_delete_artifact(db_session):
    conversation = create_conversation()
    db_session.add(conversation)
    db_session.commit()

    repo = ArtifactRepository(db_session)

    artifact = create_artifact(conversation.id)

    repo.add(artifact)
    db_session.commit()

    repo.delete(artifact)
    db_session.commit()

    assert repo.get(artifact.id) is None

def test_list_by_conversation(db_session):
    conversation1 = create_conversation()
    conversation2 = create_conversation()

    db_session.add_all([conversation1, conversation2])
    db_session.commit()

    repo = ArtifactRepository(db_session)

    repo.add(create_artifact(conversation1.id, "a.py"))
    repo.add(create_artifact(conversation1.id, "b.py"))
    repo.add(create_artifact(conversation2.id, "c.py"))

    db_session.commit()

    artifacts = repo.list_by_conversation(conversation1.id)

    assert len(artifacts) == 2

    filenames = {artifact.filename for artifact in artifacts}

    assert filenames == {"a.py", "b.py"}


def test_count_artifacts(db_session):
    conversation = create_conversation()

    db_session.add(conversation)
    db_session.commit()

    repo = ArtifactRepository(db_session)

    repo.add(create_artifact(conversation.id))
    repo.add(create_artifact(conversation.id, "test.py"))

    db_session.commit()

    assert repo.count() == 2