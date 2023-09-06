from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app=app)

def test_booking():
   response = client.post('/booking', json ={ "patname" : "v", "patage" : "","patproblem" : "","MobileNo" : "000000000","did" : "integer","wday" : "19@34","sid" :"10","pid" : "8"})
   assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
   response2 = client.post('/booking', json ={ "patname" : "", "patage" : "seven","patproblem" : "","MobileNo" : "7865457865","did" : "star","wday" : "29-02-2022","sid" :"98","pid" : "56"})
   assert response2.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY