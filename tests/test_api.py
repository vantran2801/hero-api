def test_list_heroes_returns_seeded_heroes(seeded_client):
    response = seeded_client.get("/api/v1/heroes")

    assert response.status_code == 200
    assert len(response.json()) == 4


def test_get_hero_returns_expected_hero(seeded_client):
    response = seeded_client.get("/api/v1/heroes/1")

    assert response.status_code == 200
    assert response.json()["name"] == "Tony"
    assert response.json()["status"] == "active"
    assert "created_at" in response.json()


def test_create_hero_rejects_invalid_age(client):
    response = client.post(
        "/api/v1/heroes",
        json={"name": "Invalid", "age": -5, "secret_name": "Invalid Hero"},
    )

    assert response.status_code == 422


def test_create_hero_rejects_unknown_team(client):
    response = client.post(
        "/api/v1/heroes",
        json={
            "name": "Unknown Team",
            "age": 30,
            "secret_name": "Unknown",
            "team_id": 999,
        },
    )

    assert response.status_code == 400


def test_duplicate_team_returns_conflict(client):
    payload = {"name": "Avengers", "headquarters": "New York"}

    assert client.post("/api/v1/teams", json=payload).status_code == 201
    duplicate = client.post("/api/v1/teams", json=payload)

    assert duplicate.status_code == 409


def test_team_heroes_returns_not_found_for_unknown_team(client):
    response = client.get("/api/v1/teams/999/heroes")

    assert response.status_code == 404
