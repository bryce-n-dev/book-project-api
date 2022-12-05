from fastapi.testclient import TestClient
import json

from main import app

client = TestClient(app)

data = {
    "isbn": "testbook",
    "user_id": "testuser"
}

def test_get_user():
    response = client.get('/users/bogus1')
    assert response.status_code == 200
    assert response.json() == {
        "user_id": "bogus1",
        "name": "guy"
    }


def test_get_invalid_user():
    response = client.get('/users/not_a_real_user')
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_get_favourites():
    response = client.get('/users/bogus1/favourites/')
    assert response.status_code == 200


def test_get_books():
    response = client.get('/books')
    assert response.json()
    #assert response.status_code == 200


def test_get_user_shelf():
    response = client.get('/users/bogus1/shelves/1')
    assert response.status_code == 200


def test_get_user_book():
    response = client.get('/users/bogus1/books/9780553573398')
    assert response.status_code == 200
    assert response.json()["isbn"] == '9780553573398'

def test_get_invalid_book():
    response = client.get('/users/bogus1/books/9780765311700')
    assert response.status_code == 404
    assert response.json() == {"detail": "User book not found"}


def test_update_user_book():
    response = client.put('/users/bogus1/books/9780312330873', json = {
        "isbn":  "9780312330873",
        "user_id": "bogus1",
        "shelf_id": "2"
    })
    assert response.status_code == 200
    assert response.json()["shelf_id"] == 2

def test_create_user_book():
    response = client.post("/users/bogus1/books/", json = {
        "isbn":  "9782253140870",
        "user_id": "bogus1",
        "shelf_id": "2"
    })
    assert response.status_code == 200
    assert response.json()["isbn"] == '9782253140870'


def test_delete_user_book():
    response = client.delete("/users/bogus1/books/9782253140870")
    assert response.status_code == 200
