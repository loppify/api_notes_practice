from datetime import timedelta

from app.api.auth import decode_access_token
from app.models.tag import Tag
from app.models.task import Task
from app.utils.auth import create_access_token, get_password_hash, verify_password


def test_password_hashing():
    raw_password = "password123/\\"
    hashed_password = get_password_hash(raw_password)

    assert hashed_password != raw_password
    assert verify_password(raw_password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False


def test_access_token():
    data = {"sub": "1"}
    jwt = create_access_token(data=data, expires_delta=timedelta(minutes=20))

    decoded = decode_access_token(jwt)
    assert decoded.model_dump()["username"] == data["sub"]


def test_tag_amount_property():
    tag = Tag(name="Backend", description="Testtesttest")
    assert tag.amount == 0

    tag.tasks = [
        Task(title="task1", description="abc"),
        Task(title="task3", description="abc"),
        Task(title="task2", description="abc"),
    ]
    assert tag.amount == 3
