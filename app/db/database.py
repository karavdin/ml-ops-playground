from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import URL

from contextlib import contextmanager
import os

# should be changed in env, configured outside
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/db"
print(os.environ['SQLALCHEMY_DATABASE_URL'])
SQLALCHEMY_DATABASE_URL = os.environ['SQLALCHEMY_DATABASE_URL']
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = scoped_session(sessionmaker(
    bind=engine, expire_on_commit=False))
Base = declarative_base()


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
