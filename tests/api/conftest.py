from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.conversation import get_conversation_service


@pytest.fixture
def mock_conversation_service():
    return MagicMock()


@pytest.fixture
def client(mock_conversation_service):
    app.dependency_overrides[get_conversation_service] = (
        lambda: mock_conversation_service
    )

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()