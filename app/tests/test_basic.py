from fastapi.testclient import TestClient

def test_get(client: TestClient):
    response = client.get('/documents', params={'query': 'девушки'})
    assert response.status_code == 200
