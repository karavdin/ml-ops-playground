from sqlalchemy import create_engine, SQLModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@postgresserver/db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/db"

url = URL.create(
    drivername="postgresql",
    username="postgres",
    host="localhost:5432",
    database="db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# def init_db():
#     Base.metadata.create_all(engine)


# def init_db():
#     SQLModel.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
