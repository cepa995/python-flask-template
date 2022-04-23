from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def get_engine(user, passwd, host, port, db, postgresql=False):
    """
    Retrive SQLAclhemy engine 

    :param user   - DB username
    :param passwd - DB password
    :param host   - DB host
    :param port   - DB Port
    :param db     - DB name
    """
    if postgresql:
        url = "postgresql://%s:%s@%s:%d/%s" % (user, passwd, host, port, db)
        engine = create_engine(url, pool_size=50, echo=False)
    else:
        engine = create_engine('sqlite:////tmp/docgen.db')
    return engine

engine     = get_engine(user='postgres',passwd='postgres',host='localhost',port=8080,db='docgen')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base       = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """ Initialize the database """
    import app.mod_doc.models
    import app.mod_auth.models
    
    Base.metadata.create_all(bind=engine)
