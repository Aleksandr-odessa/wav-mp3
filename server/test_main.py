from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    responce = client.get("/")
    assert responce.status_code == 200
    assert responce.json() == {"message": "welcome to services wav to audio"}


def test_add_user():
    responce = client.post("/users", json={'name': 'test1'})
    assert responce.status_code == 201
    responce_duble = client.post("/users", json={'name': 'test'})
    assert responce_duble.status_code == 400
