import os
import tempfile

import pytest
from app import create_app
from app.db import init_db, db_session

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

"""
NOTE: PyTest uses fixtures by matching their function names with the names of arguments in the test functions. For example,
the test_welcome (in test_factory.py) function takes a client argument. Pytest matches that with the client fixuture function
(in this file), calls it, and passes the returned value to the test function.
"""

@pytest.fixture
def app():
    # Creates and opens a temporary file, returning the file descriptor and path to it
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,     # TESTING Tells Flask that the app is in test mode. Flask changes some internal ebhavior so its easier to test
        'DATABASE': db_path, # DATABASE path is overriden so it points ot previously created temporary path instead of the instance folder
    })

    # Instantiate the databse and insert data
    with app.app_context():
        init_db()
        db_session.executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """ Application object gets created by the app fixture. Tests will use the cleint to 
    make requests to the application without running the server """
    return app.test_client()

@pytest.fixture
def runner(app):
    """ Creates a runner that can call the Click commands registered with the application """
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)