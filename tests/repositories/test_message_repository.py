from uuid import uuid4

from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.db.repositories.message_repository import MessageRepository


def create_conversation():
    return Conversation(
        request_id=uuid4(),
        user_query="Test Conversation",
    )


def create_message(
    conversation_id,
    role="user",
    content="Hello",
    agent_name="User",
):
    return Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        agent_name=agent_name,
    )


def test_add_and_get_message(db_session):
    conversation = create_conversation()

    db_session.add(conversation)
    db_session.commit()

    repo = MessageRepository(db_session)

    message = create_message(conversation.id)

    repo.add(message)
    db_session.commit()

    fetched = repo.get(message.id)

    assert fetched is not None
    assert fetched.id == message.id
    assert fetched.content == "Hello"


def test_get_non_existing_message(db_session):
    repo = MessageRepository(db_session)

    assert repo.get(uuid4()) is None


def test_delete_message(db_session):
    conversation = create_conversation()

    db_session.add(conversation)
    db_session.commit()

    repo = MessageRepository(db_session)

    message = create_message(conversation.id)

    repo.add(message)
    db_session.commit()

    repo.delete(message)
    db_session.commit()

    assert repo.get(message.id) is None


def test_list_by_conversation(db_session):
    conversation1 = create_conversation()
    conversation2 = create_conversation()

    db_session.add_all([conversation1, conversation2])
    db_session.commit()

    repo = MessageRepository(db_session)

    repo.add(create_message(conversation1.id, content="First"))
    repo.add(create_message(conversation1.id, content="Second"))
    repo.add(create_message(conversation2.id, content="Third"))

    db_session.commit()

    messages = repo.list_by_conversation(conversation1.id)

    assert len(messages) == 2

    contents = [message.content for message in messages]

    assert contents == ["First", "Second"]


def test_count_messages(db_session):
    conversation = create_conversation()

    db_session.add(conversation)
    db_session.commit()

    repo = MessageRepository(db_session)

    repo.add(create_message(conversation.id))
    repo.add(create_message(conversation.id, content="Another"))

    db_session.commit()

    assert repo.count() == 2