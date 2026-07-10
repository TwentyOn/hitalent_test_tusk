from unittest.mock import patch

import pytest


@pytest.mark.parametrize('doc_id, status_code', [
    (20, 204),
    (9999, 404)
])
@pytest.mark.asyncio
async def test_delete(client, doc_id: int, status_code: int, fill):
    with patch('routers.documents.INDEX_NAME', 'test_documents'):
        response = await client.delete(f'/documents/{doc_id}')
        assert response.status_code == status_code
