from unittest.mock import patch

import pytest

@pytest.mark.asyncio
async def test_get(client, fill_data):
    with patch('routers.documents.INDEX_NAME', 'test_documents'):
        response = await client.get('/documents', params={'query': 'девушки'})
        content = response.json()
        assert response.status_code == 200
        assert len(content) <= 20
        assert {'id', 'rubrics', 'text', 'created_date'} == content[0].keys()
        assert content[0]['created_date'] > content[-1]['created_date']
