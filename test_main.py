from fastapi.testclient import TestClient


from main import app


# Each of these unit test functions below will get run when calling the `pytest` command.
# Each test requires minimal explanation.
# We first make a request to the API using the test client.
# The test client returns a response that we then validate by using the Python `assert` keyword.

# Create a client for testing purposes
client = TestClient(app)

# Create fake data to be used in some of the unit tests.
data = {
    "isbn":  "9780312330873",
    "user_id": "bogus1",
    "shelf_id": "2"
}

# Test that user is returned
def test_get_user():
    response = client.get('/users/bogus1')
    assert response.status_code == 200
    assert response.json() == {
        "user_id": "bogus1",
        "name": "guy"
    }

# Test that user is invalid
def test_get_invalid_user():
    response = client.get('/users/not_a_real_user')
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

# Test that returns favourite books
def test_get_favourites():
    response = client.get('/users/bogus1/favourites/')
    assert response.status_code == 200

# Test that returns all books
def test_get_books():
    response = client.get('/books')
    assert response.json()
    # assert response.status_code == 200

# Test that returns user shelf
def test_get_user_shelf():
    response = client.get('/users/bogus1/shelves/1')
    assert response.status_code == 200

# Test that returns user book information
def test_get_user_book():
    response = client.get('/users/bogus1/books/9780553573398')
    assert response.status_code == 200
    assert response.json()["isbn"] == '9780553573398'

# Test that book is invalid
def test_get_invalid_book():
    response = client.get('/users/bogus1/books/9780765311700')
    assert response.status_code == 404
    assert response.json() == {"detail": "User book not found"}

# Test that modifies book information
def test_update_user_book():
    response = client.put('/users/bogus1/books/9780312330873', json = {
        "isbn":  "9780312330873",
        "user_id": "bogus1",
        "shelf_id": "2"
    })
    assert response.status_code == 200
    assert response.json()["shelf_id"] == 2

# Test that creates a book
def test_create_user_book():
    response = client.post("/users/bogus1/books/", json = {
        "isbn":  "9782253140870",
        "user_id": "bogus1",
        "shelf_id": "2"
    })
    assert response.status_code == 200
    assert response.json()["isbn"] == '9782253140870'

# Test that removes user book
def test_delete_user_book():
    response = client.delete("/users/bogus1/books/9782253140870")
    assert response.status_code == 200
