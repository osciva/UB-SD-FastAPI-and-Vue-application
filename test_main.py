from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_delete_team():
    # eliminem al barça
    team_name = "Barça"
    response = client.delete(f"/teams/{team_name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"{team_name} has been deleted successfully."}

    # comprovem que no estigui
    response = client.get("/teams/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert {"team_name": "Barça"} not in response.json()

def test_update_team():
    response = client.put("/team/Barça", json={"name": "Barça", "country": "Spain", "description": "Més que un club"})
    assert response.status_code == 200
    assert response.json()['name'] == "Barça"
    assert response.json()['country'] == "Spain"
    assert response.json()['description'] == "Més que un club"

    response = client.put("/team/Juventus", json={"name": "Juventus FC", "country": "Italy"})
    assert response.status_code == 200
    assert response.json()['name'] == "Juventus FC"
    assert response.json()['country'] == "Italy"
    assert response.json()['description'] == None

