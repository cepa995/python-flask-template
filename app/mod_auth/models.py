# Import the database object (db) from the main application module
from sqlalchemy import Column, Integer, SmallInteger, String
from app.db import Base

# Define a User model
class User(Base):
    __tablename__ = 'users'

    id       = Column(Integer, primary_key=True)
    # Identification Data:
    username     = Column(String(128),  nullable=False, unique=True,)
    # Password
    password = Column(String(192),  nullable=False)
    # Authorisation Data: role & status
    role     = Column(SmallInteger, nullable=False)
    status   = Column(SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, username, password, role=1, status=1):
        self.username     = username
        self.password     = password
        self.role         = role
        self.status       = status

    def __repr__(self):
        return '<%r>' % (self.username) 