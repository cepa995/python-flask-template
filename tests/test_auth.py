import pytest

from flask import g, session
from app.db import get_db


def test_register(client, app):
    """ Test user registration handler """
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'abc', 'password': 'def'}
    )
    assert "/auth/login" in response.headers["Location"] 

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'abc'",
        ).fetchone() is not None

# Here we tell Flask to run same test function (i.e., test_register_validate_input) but with different arguments.
@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    """ Tests user registration with different parameters 
    
    :param client   - PyTest client fixture
    :param username - user username
    :param password - user password
    :param message  - validation message
    """
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    """ Tests user login handler
    
    :param client - PyTest client fixture
    :param auth   - PyTest fixture which returns instance of AuthActions class
    """
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get('/')
        print('B')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    """ Tests user login with different parameters 
    
    :param client   - PyTest client fixture
    :param username - user username
    :param password - user password
    :param message  - validation message
    """
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    """ Tests user logout handler
    
    :param client - PyTest client fixture
    :param auth   - PyTest fixture which returns instance of AuthActions class
    """
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session
