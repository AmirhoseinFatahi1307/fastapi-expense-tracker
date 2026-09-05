from sqlalchemy import create_engine

from core.config import settings

from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # only for sqlite
)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_de():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
