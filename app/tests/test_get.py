import pytest
from fastapi.testclient import TestClient

def test_get(client: TestClient):
    response = client.get('/documents', params={'query': 'девушки'})
    content = response.json()
    assert response.status_code == 200
    assert len(content) == 20
    assert content['count'] == 1

@pytest.mark.parametrize('doc_id, status_code', [
    (1, 204),
    (1501, 404)
])
def test_delete(client: TestClient, doc_id: int, status_code: int):
    response = client.delete(f'/documents/{doc_id}/')
    assert response.status_code == status_code
