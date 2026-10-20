import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.database import get_session
from app.main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def seeded_client(client):
    team = client.post(
        "/api/v1/teams",
        json={"name": "Avengers", "headquarters": "New York"},
    ).json()
    for name, age in [("Tony", 45), ("Natasha", 35), ("Steve", 105), ("Peter", 16)]:
        response = client.post(
            "/api/v1/heroes",
            json={
                "name": name,
                "age": age,
                "secret_name": f"{name} Secret",
                "team_id": team["id"],
            },
        )
        assert response.status_code == 201
    return client
