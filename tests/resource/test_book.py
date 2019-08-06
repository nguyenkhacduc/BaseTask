# Import the resources/controllers we're testing
from source.resources.api import *

# client is a fixture, injected by the `pytest-flask` plugin
def test_get_book(client):
    # Make a tes call to /books/1
    response = client.get("api/books/1")

    # Validate the response
    assert response.status_code == 200