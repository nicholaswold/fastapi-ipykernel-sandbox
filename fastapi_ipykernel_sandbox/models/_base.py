from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DatabaseModel = declarative_base()

_engine = create_engine('sqlite:///sandbox.db', echo=True)
_session_factory = sessionmaker(bind=_engine)

def db_session():
    session = _session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def create_tables():
    DatabaseModel.metadata.create_all(_engine)

def drop_tables():
    DatabaseModel.metadata.drop_all(_engine)
