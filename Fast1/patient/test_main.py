from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app=app)

def test_get_all_patient():
    response = client.get('/patient')
    try:
        assert response.status_code == status.HTTP_200_OK
    except AssertionError:
        raise
def test_login():
    response = client.post('/login',json={"username":"veda@gmail.com","password":"veda123"})
    assert response.status_code == status.HTTP_200_OK
    response3 = client.post('/login',json={"username":"","password":"veda123"})
    assert response3.status_code == status.HTTP_404_NOT_FOUND
    response4 = client.post('/login',json={"username":"veda","password":"veda"})
    assert response4.status_code == status.HTTP_404_NOT_FOUND
    