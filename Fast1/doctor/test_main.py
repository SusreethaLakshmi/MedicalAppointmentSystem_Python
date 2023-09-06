from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app=app)

def test_get_all_doctor():
    response = client.get('/doctor')
    try:
        assert response.status_code == status.HTTP_200_OK
    except AssertionError:
        raise
def test_login():
    response = client.post('/login',json={"username":"prabhasdeva@gmail.com","password":"prabhas123"})
    assert response.status_code == status.HTTP_200_OK
    response3 = client.post('/login',json={"username":"","password":"prabhas123"})
    assert response3.status_code == status.HTTP_404_NOT_FOUND
    response4 = client.post('/login',json={"username":"prabhasdeva","password":"veda"})
    assert response4.status_code == status.HTTP_404_NOT_FOUND
    