from uuid import uuid4

from app.db.models.conversation import Conversation, ConversationStatus
from app.db.repositories.conversation_repository import ConversationRepository


def create_conversation(
    query="Test Query",
    status=ConversationStatus.RUNNING,
):
    return Conversation(
        request_id=uuid4(),
        user_query=query,
        status=status,
    )


def test_add_and_get_conversation(db_session):
    repo = ConversationRepository(db_session)

    conversation = create_conversation()

    repo.add(conversation)
    db_session.commit()

    fetched = repo.get(conversation.id)

    assert fetched is not None
    assert fetched.id == conversation.id
    assert fetched.user_query == "Test Query"


def test_get_non_existing_conversation(db_session):
    repo = ConversationRepository(db_session)

    conversation = repo.get(uuid4())

    assert conversation is None


def test_delete_conversation(db_session):
    repo = ConversationRepository(db_session)

    conversation = create_conversation()

    repo.add(conversation)
    db_session.commit()

    repo.delete(conversation)
    db_session.commit()

    assert repo.get(conversation.id) is None


def test_list_conversations(db_session):
    repo = ConversationRepository(db_session)

    repo.add(create_conversation("First"))
    repo.add(create_conversation("Second"))
    repo.add(create_conversation("Third"))

    db_session.commit()

    conversations = repo.list(page=1, page_size=10)

    assert len(conversations) == 3


def test_count_conversations(db_session):
    repo = ConversationRepository(db_session)

    repo.add(create_conversation(status=ConversationStatus.RUNNING))
    repo.add(create_conversation(status=ConversationStatus.COMPLETED))
    repo.add(create_conversation(status=ConversationStatus.COMPLETED))

    db_session.commit()

    assert repo.count() == 3
    assert repo.count_by_status(ConversationStatus.RUNNING) == 1
    assert repo.count_by_status(ConversationStatus.COMPLETED) == 2
    assert repo.count_by_status(ConversationStatus.FAILED) == 0


def test_list_with_query_filter(db_session):
    repo = ConversationRepository(db_session)

    repo.add(create_conversation("Generate Login API"))
    repo.add(create_conversation("Weather App"))

    db_session.commit()

    conversations = repo.list(
        page=1,
        page_size=10,
        query="Login",
    )

    assert len(conversations) == 1
    assert conversations[0].user_query == "Generate Login API"


def test_list_with_status_filter(db_session):
    repo = ConversationRepository(db_session)

    repo.add(create_conversation(status=ConversationStatus.RUNNING))
    repo.add(create_conversation(status=ConversationStatus.COMPLETED))

    db_session.commit()

    conversations = repo.list(
        page=1,
        page_size=10,
        status=ConversationStatus.RUNNING,
    )

    assert len(conversations) == 1
    assert conversations[0].status == ConversationStatus.RUNNING