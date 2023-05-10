import models
from main import app, get_db
from fastapi.testclient import TestClient
import schemas
from schemas import *

client = TestClient(app)
db = next(get_db())


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# ----------------------------------------TESTS-DE-TEAMS---------------------------------------

# test para crear un equipo
def test_create_team():
    # Crea un equipo
    team = {"name": "Madrid", "country": "Spain", "description": "Futbol Team"}
    response = client.post("/teams/", json=team)
    assert response.status_code == 200

    # Verifica que la respuesta tenga la información correcta del equipo creado
    assert response.json()["name"] == team["name"]
    assert response.json()["country"] == team["country"]
    assert response.json()["description"] == team["description"]
    assert response.json()["id"]


# test para leer todos los equipos
def test_read_teams():
    response = client.get("/teams/")
    assert response.status_code == 200
    # comprovamos que devuelva una lista de equipos
    assert isinstance(response.json(), list)


# test para obtener un equipo dado su nombre
def test_read_team_by_name():
    teamname = "Madrid"
    # Leer el equipo
    response = client.get(f"/team/{teamname}")
    assert response.status_code == 200
    assert response.json()["name"] == "Madrid"
    assert response.json()["country"] == "Spain"
    assert response.json()["description"] == "Futbol Team"


# test para eliminar un equipo
def test_delete_team():
    team = "Madrid"
    teams = {
        "name": "Madrid",
        "country": "Spain",
        "description": None
    }
    response = client.post("/teams/", json=teams)
    assert response.status_code == 200
    team_id = response.json()["id"]
    team_to_delete = {
        "name": "Madrid",
        "country": "Spain",
        "description": None,
        "id": team_id
    }
    response = client.delete(f"/teams/{team}", json=team_to_delete)
    assert response.status_code == 200
    assert response.json()["name"] == team


# test para actualizar un equipo
def test_update_team():
    # Crear un equipo para actualizar
    team = {"name": "madrid", "country": "Spain", "description": "HALA MADRIIID"}
    response = client.post("/teams/", json=team)
    assert response.status_code == 200

    # Verifica que la respuesta tenga la información correcta del equipo creado
    assert response.json()["name"] == team["name"]
    assert response.json()["country"] == team["country"]
    assert response.json()["description"] == team["description"]
    assert response.json()["id"]


    # Actualizar el equipo con un nombre y una descripción diferentes
    response = client.put("/team/Madrid",
                          json={"name": "Barça", "country": "Spain", "description": "Mejor que el Madrid"})
    # Verificar que el equipo ha sido actualizado correctamente
    assert response.status_code == 200
    assert response.json()["name"] == "Barça"
    assert response.json()["country"] == "Spain"
    assert response.json()["description"] == "Mejor que el Madrid"


# ----------------------------------------TESTS-DE-COMPETITIONS---------------------------------------


# Test para crear una competición
def test_create_competition():
    # Crear y añadir competición
    team_info = {
        "name": "barça3",
        "country": "catalonia",
        "description": "més que un club"
    }
    response = client.post("/teams/", json=team_info)
    print(response)
    team_id = response.json()["id"]

    teams_to_add = Team(name="barça3", country="catalonia", description="més que un club", id=team_id)
    new_competition = {
        "name": "Primera division",
        "category": "professional",
        "sport": "football",
        "teams": [teams_to_add.dict()]
    }
    response = client.post("/competitions/", json=new_competition)

    assert response.status_code == 200
    assert response.json()["name"] == "Primera division"
    assert response.json()["category"] == "professional"
    assert response.json()["sport"] == "football"
    assert response.json()["teams"][0]["name"] == "barça3"

# test para leer todas las competitions
def test_read_competitions():
    response = client.get("/competitions/")
    assert response.status_code == 200
    # comprovamos que devuelva una lista de competitions
    assert isinstance(response.json(), list)


# Test para obtener una competición por su id
def test_read_competition_by_id():
    id = 1
    # Leer el equipo
    response = client.get(f"/competitions/{id}")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Primera division",
        "category": "professional",
        "sport": "football"
    }




# Test para actualizar una competición
def test_update_competition():
    # Crear un equipo para actualizarlo después
    new_competition4 = {"id": 4, "name": "LigaMx", "category": "professional", "sport": "football",
                        "teams": ["Mexico"]}
    response = client.post("/competitions/", json=new_competition4)
    assert response.status_code == 200
    assert response.json() == new_competition4
    assert response.json()["id"] == 4
    assert response.json()["name"] == "LigaMx"
    assert response.json()["category"] == "professional"
    assert response.json()["sport"] == "football"
    assert response.json()["teams"] == ["Mexico"]

    # Actualizar el equipo
    updated_competition4 = {"id": 4, "name": "LigaMx", "category": "amateur", "sport": "football",
                            "teams": ["Mexico", "Venecia"]}

    response = client.put("/competitions/LigaMx", json=updated_competition4)

    assert response.status_code == 200
    assert response.json()["id"] == 4
    assert response.json()["name"] == "LigaMx"
    assert response.json()["category"] == "amateur"
    assert response.json()["sport"] == "football"
    assert response.json()["teams"] == ["Mexico", "Venecia"]


# Test para eliminar una competición (este con el id va y el anterior no... en fin)
def test_delete_competition():
    # Crear una competición para luego borrarla
    new_competition5 = {"id": 5, "name": "BBVA", "category": "professional", "sport": "football",
                        "teams": ["Madrid", "Barça"]}
    response = client.post("/competitions/", json=new_competition5)
    assert response.status_code == 200
    assert response.json() == new_competition5

    # Borrar la competición
    response = client.delete("/competitions/5")

    # Comprobar que se ha eliminado correctamente
    assert response.status_code == 200
    assert response.json() == {"message": "5 has been deleted successfully."}

    # Y comprobar ya no están sus datos
    response = client.get("/competitions/5")
    assert response.status_code == 404


# ----------------------------------------TESTS-DE-MATCHES---------------------------------------

def test_read_matches():
    response = client.get("/matches/")
    assert response.status_code == 200
    # comprovamos que devuelva una lista de matches
    assert isinstance(response.json(), list)


"""# Test para crear un match
def test_create_match():
    teams_to_add = Team(name="barça3", country="catalonia", description="més que un club", id=1)
    new_competition = {
        "name": "Primera division",
        "category": "professional",
        "sport": "football",
        "teams": [teams_to_add.dict()]
    }
    local_team = Team(name="barça3", country="catalonia", description="més que un club", id=1).dict()
    visitor_team = Team(name="espanyol", country="catalonia", description="més que un club", id=2).dict()

    new_match2 = {
        "date": "2023-04-11T13:30:00",
        "price": 40.20,
        "competition": new_competition,
        "local": local_team,
        "visitor": visitor_team

        #"competition": "Primeradivision",
        #"local": "barça3",
        #"visitor": "espanyol
    }
    print("before create_match")
    response = client.post("/matches", json=new_match2)
    print("reeeeeesponse", response)
    assert response.status_code == 200

    #assert response.json()["date"] == new_match2["date"]
    #assert response.json()["price"] == new_match2["price"]
    #assert response.json()["competition"] == new_match2["Primera division"]
    #assert response.json()["local"] == new_match2["Espanyol_00"]
    #assert response.json()["visitor"] == new_match2["Barçaaaaa"]"""

def test_create_match():
    # Creamos dos equipos
    local_team = {
        "name": "barça3",
        "country": "catalonia",
        "description": "més que un club",
        "id": 1
    }
    visitor_team = {
        "name": "espanyol",
        "country": "catalonia",
        "description": "som la gent blanqu-i-blava",
        "id": 2
    }

    # Creamos una nueva competición
    new_competition = {
        "name": "Primera division",
        "category": "Senior",
        "sport": "Football",
        "teams": [local_team, visitor_team],
        "id": 1
    }

    # Creamos un nuevo partido
    new_match = {
        "date": "2019-05-11T13:30:00",
        "price": 1.20,
        "competition": new_competition,
        "local": local_team,
        "visitor": visitor_team
    }

    # Enviamos la petición HTTP al servidor
    response = client.post("/matches/", json=new_match)
    print(response.json())

    # Comprobamos que se ha creado el partido correctamente
    assert response.status_code == 200

    match = response.json()
    assert match["date"] == "2019-05-11T13:30:00"
    assert match["price"] == 1.20
    assert match["competition"]["name"] == "Primera division"
    assert match["local"]["name"] == "barça3"
    assert match["visitor"]["name"] == "espanyol"



# Test de encontrar un match a traves de su id
def test_read_match_by_id():
    # Agregar match de prueba
    new_match = {'id': 1,
                 'local': "UBSport",
                 'visitor': 'UPC sport',
                 'date': '2023-04-15',
                 'price': 40.20}
    response = client.post("/matches/", json=new_match)
    assert response.status_code == 200
    assert response.json() == new_match

    # Acceder al match creado
    response2 = client.get("/matches/1")
    assert response2.status_code == 200
    assert response2.json() == new_match


# Test para actualizar un match
def test_update_match():
    # Crear un match para actualizarlo después
    new_match3 = {'id': 3,
                  'local': "Espanyol",
                  'visitor': 'Barça',
                  'date': '2023-05-14',
                  'price': 95.50}
    response = client.post("/matches/", json=new_match3)
    assert response.status_code == 200
    assert response.json() == new_match3
    assert response.json()["id"] == 3
    assert response.json()["local"] == "Espanyol"
    assert response.json()["visitor"] == "Barça"
    assert response.json()["date"] == "2023-05-14"
    assert response.json()["price"] == 95.50

    # Actualizar el match
    updated_match3 = {'id': 3,
                      'local': "Espanyol",
                      'visitor': 'Girona',
                      'date': '2023-05-14',
                      'price': 66.50}

    response = client.put("/matches/3", json=updated_match3)

    assert response.status_code == 200
    assert response.json()["id"] == 3
    assert response.json()["local"] == "Espanyol"
    assert response.json()["visitor"] == "Girona"
    assert response.json()["date"] == "2023-05-14"
    assert response.json()["price"] == 66.50


# Test para eliminar un match
def test_delete_match():
    # Crear una match para luego borrarla
    new_match4 = {'id': 4,
                  'local': "Sevilla",
                  'visitor': 'Getafe',
                  'date': '2023-01-10',
                  'price': 16.50}
    response = client.post("/matches/", json=new_match4)
    assert response.status_code == 200
    assert response.json() == new_match4

    # Borrar el match
    response = client.delete("/matches/4")

    # Comprobar que se ha eliminado correctamente
    assert response.status_code == 200
    assert response.json() == {"message": "4 has been deleted successfully."}

    # Y comprobar ya no están sus datos
    response = client.get("/matches/4")
    assert response.status_code == 404
