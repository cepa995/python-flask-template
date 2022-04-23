import sqlite3

import pytest
from app.db import get_db


def test_get_close_db(app):
    """ Tests Database Connection """
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)
