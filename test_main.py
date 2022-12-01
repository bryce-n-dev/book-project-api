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
    response = client.get('users/not_a_real_user')
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_get_favourites():
    response = client.get('/users/bogus1/favourites')
    assert response.status_code == 200
    assert response.json()["isbn"] == 9780765311788

    pass

def test_get_books():
    response = client.get('/books/', json=data)
    assert response.status_code == 200
    assert data in response.json()
    pass

def test_get_user_shelf():
    response = client.get('/users/bogus1/shelves/1')
    assert response.status_code == 200
    assert response.json() == [
      {
        "UserBook": {
          "isbn": "9780063021426",
          "pages_read": null,
          "date_finished_reading": null,
          "review": null,
          "shelf_id": 1,
          "user_id": "1234",
          "date_started_reading": null,
          "rating": null,
          "is_favourite": false
        },
        "BookInfo": {
          "title": "Babel, Or the Necessity of Violence: An Arcane History of the Oxford Translators’ Revolution",
          "year": 2022,
          "cover_url": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1664641157i/57945316.jpg",
          "series_pos": 1,
          "publisher_id": "hc",
          "genre_id": "fts",
          "blurb": "Traduttore, traditore: An act of translation is always an act of betrayal.",
          "isbn": "9780063021426",
          "page_no": 545,
          "author_id": "rfk",
          "language_id": "en"
        },
        "name": "R. F. Kuang",
        "genre": "Fantasy"
      }
    ]
    pass

def test_get_user_book():
    response = client.get('/users/bogus1/books/')
    assert response.status_code == 200
    assert response.json() == {
        "isbn": "book1",
        "user_id": "user1",
        "shelf_id": "123",
        "pages_read": "123",
        "date_started_reading": "01/01/01",
        "date_finished_reading": "01/01/01",
        "rating": "3",
        "review": "good",
        "is_favourite": "false"
    }
    pass

def test_update_user_book():
    response = client.put('/users/bogus1/books/')
    assert response.status_code == 200
    pass

def test_delete_user_book():
    #isbn = user_book.isbn
    #delete_user_book(isbn)

    response = client.delete("/users/bogus1/books/")
    assert response.status_code == 200

    pass

def test_create_user_book():
    response = client.post("/users/bogus1/books/", json = data)
    assert response.status_code == 200
    assert response.json() == data
