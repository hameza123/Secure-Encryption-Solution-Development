# test_routes.py

from app import create_app
import pytest

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Bienvenue sur l'application de chiffrement" in response.data
