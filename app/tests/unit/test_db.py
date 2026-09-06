import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import User


def test_user_creation():
    user = User(username="test", password="12345678", email="test")

    assert user.username == "test"
    assert user.password == "12345678"
    assert user.email == "test"


def test_save_and_query_user(db_session):
    user = User(username="test", password="111111", email="test")
    db_session.add(user)
    db_session.flush()

    retrieved_user = db_session.query(User).filter_by(username="test").first()

    assert retrieved_user is not None
    assert retrieved_user.username == "test"
    assert retrieved_user.id == user.id


def test_unique_username_constraint(db_session):
    db_session.add(User(username="test", password="111111111", email="test"))
    db_session.flush()

    duplicate_user = User(username="test", password="23124124", email="test2")
    db_session.add(duplicate_user)

    with pytest.raises(IntegrityError):
        db_session.flush()
