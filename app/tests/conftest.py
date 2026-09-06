import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.dao.database import Base


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection, expire_on_commit=False)
    session = Session()

    nested = connection.begin_nested()
    yield session

    session.close()
    if nested.is_active:
        nested.rollback()
    transaction.rollback()
    connection.close()
