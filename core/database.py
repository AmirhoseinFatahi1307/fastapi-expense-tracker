from sqlalchemy import create_engine

from core.config import settings

from sqlalchemy.orm import sessionmaker, declarative_base

connect_args = {}
if settings.SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
