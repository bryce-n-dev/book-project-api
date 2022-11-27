from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_user():
    response = client.get('/users/bogus1')
    assert response.status_code == 200
    assert response.json() == {
        "user_id": "bogus1",
        "name": "guy"
    }

def test_get_invalid_user():
    response = client.get('users/not_a_real_user')
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_get_favourites():
    pass

def test_get_books():
    pass

def test_get_user_shelf():
    pass

def test_get_user_book():
    pass

def test_update_user_book():
    pass

def test_delete_user_book():
    pass

def test_create_user_book():
    pass