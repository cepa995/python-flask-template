from app import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_welcome(client):
    response = client.get('/welcome')
    assert response.data == b'Hello, World!'