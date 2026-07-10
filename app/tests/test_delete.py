from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize('doc_id, status_code', [
    (20, 204),
    (9999, 404)
])
def test_delete(client: TestClient, doc_id: int, status_code: int):
    with patch('routers.documents.INDEX_NAME', 'test_documents'):
        response = client.delete(f'/documents/{doc_id}')
        assert response.status_code == status_code
