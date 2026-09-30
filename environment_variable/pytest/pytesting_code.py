from fastapi.testclient import TestClient
from API_code import app
#imporrting app object from my python code

client = TestClient(app)
#TestClient simulates an HTTP request.
#That means it acts like a real client (browser/Postman) and sends a request to your FastAPI app.

# Test /add API
def test_add_numbers():
    #The result that comes back from the API is stored in response
    response = client.get("/add?a=10&b=20")
#Check whether this condition is true.asserrt check whether the resonse is expected or not 
    assert response.status_code == 200
    assert response.json() == {"result": 30}


# Test /message API
def test_message():
    response = client.get("/message")

    assert response.status_code == 200
    assert response.json() == {"message": "Addition API is working"}