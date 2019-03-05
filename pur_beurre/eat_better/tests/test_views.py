
def test_basic(client):
    response = client.get('/eat_better/')
    assert response.status_code == 200
