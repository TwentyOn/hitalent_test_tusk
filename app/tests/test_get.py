import pytest
from fastapi.testclient import TestClient

def test_get(client: TestClient):
    response = client.get('/documents', params={'query': 'девушки'})
    content = response.json()
    assert response.status_code == 200
    assert len(content) == 20
    assert {'id', 'rubrics', 'text', 'created_date'} == content[0].keys()
    assert content[0]['created_date'] > content[-1]['created_date']
