import pytest
from fastapi.testclient import TestClient

# TODO добавить тестовую БД
# @pytest.mark.parametrize('doc_id, status_code', [
#     (18, 204),
#     (1501, 404)
# ])
# def test_delete(client, doc_id: int, status_code: int):
#
#     response = client.delete(f'/documents/{doc_id}/')
#     assert response.status_code == status_code