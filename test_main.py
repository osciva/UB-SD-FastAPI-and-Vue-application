import models
from main import app, get_db
from fastapi.testclient import TestClient
import schemas
client = TestClient(app)
db = next(get_db())

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_team():
    # Crea un equipo
    team = {"name": "Maadriiiiiiiddd", "country": "Catalonia", "description": "Futbol Team"}
    response = client.post("/teams/", json=team)
    assert response.status_code == 200

    # Verifica que la respuesta tenga la información correcta del equipo creado
    assert response.json()["name"] == team["name"]
    assert response.json()["country"] == team["country"]
    assert response.json()["description"] == team["description"]


def test_read_team_by_name():

    teamname = "barca"
    # Leer el equipo
    response = client.get(f"/team/{teamname}")
    assert response.status_code == 200
    assert response.json()["name"] == "barca"
    assert response.json()["country"] == "Country 3"
    assert response.json()["description"] == "viva el betis"



def test_delete_team():
    team_name = "Madrid"
    team_to_delete = {
        "name": "Madrid",
        "country": "Spain"
    }
    response = client.post("/teams/", json=team_to_delete)
    assert response.status_code == 200
    response = client.delete(f"/teams/{team_name}")
    assert response.status_code == 200
    assert response.json()["name"] == team_name
def test_update_team():
    # Crear un equipo para actualizar
    #client.post("/team", json={"name": "Realff Mddaeedrid", "country": "Spain", "description": "The Kings of Europe"})
    #response = client.get("/team/Barça")
    # Actualizar el equipo con un nombre y una descripción diferentes
    response = client.put("/team/Barça", json={"name": "Espanyol_00", "country": "Spain", "description": "Mejor que el Barça"})
    # Verificar que el equipo ha sido actualizado correctamente
    assert response.status_code == 200
    assert response.json()["name"] == "Espanyol_00"
    assert response.json()["country"] == "Spain"
    assert response.json()["description"] == "Mejor que el Barça"


# Test para obtener una competición por su nombre
#def test_read_competition_by_name():
    # Agregar competición de prueba
    #new_competition ={"id":1, "name": "SerieA", "category": "professional", "sport": "football", "teams": ["AC Milan", "Inter Milan"]}
    #response = client.post("/competitions/", json=new_competition)
    #assert response.status_code == 200
    #assert response.json() == new_competition

    # Hacer petición GET
    #response = client.get("/competitions/SerieA")


    # Verificar que la petición fue exitosa y que se obtuvo la competición correcta
    #assert response.status_code == 200
    #assert response.json() == new_competition


# Test para obtener una competición por su nombre
#def test_read_competition_by_name():
    # Agregar competición de prueba
    #new_competition ={"id":1, "name": "SerieA", "category": "professional", "sport": "football", "teams": ["AC Milan", "Inter Milan"]}
    #response = client.post("/competitions/", json=new_competition)
    #assert response.status_code == 200
    #assert response.json() == new_competition

    # Hacer petición GET
    #response = client.get("/competitions/SerieA")


    # Verificar que la petición fue exitosa y que se obtuvo la competición correcta
    #assert response.status_code == 200
    #assert response.json() == new_competition

# Test para obtener una competición por su id
def test_read_competition_by_id():
    # Agregar competición de prueba
    new_competition2 ={"id": 2, "name": "BBVA", "category": "professional", "sport": "football", "teams": ["Madrid", "Barça"]}
    response = client.post("/competitions/", json=new_competition2)
    assert response.status_code == 200
    assert response.json() == new_competition2

    # Acceder a la competición creada
    response2 = client.get("/competitions/2")
    #PROBLEMA: no entiende el ID en la URL?
    assert response2.status_code == 200
    assert response2.json() == new_competition2


# Test para crear una competición
def test_create_competition():
    # Crear y añadir competición
    new_competition ={
        "name": "Primera division",
        "category": "professional",
        "sport": "football",
        "teams": [
            {
                "name": "Team id 2",
                "country": "Country 3",
                "description": "New description of Team id 2 with Country 3",
                "id": 1
            },
            {
                "name": "barca",
                "country": "Country 3",
                "description": "viva el betis",
                "id": 2
            },

        ]
    }
    response = client.post("/competitions/", json=new_competition)
    print(response)
    assert response.status_code == 200
    assert response.json()["name"] == new_competition["name"]
    assert response.json()["category"] == new_competition["category"]
    assert response.json()["sport"] == new_competition["sport"]
    assert response.json()["teams"] == new_competition["teams"]



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
                        "teams": ["Mexico","Venecia"]}
    # PROBLEMA: el servidor no puede entender la solicitud del
    # cliente debido a un error en la sintaxis o formato de los datos enviados.
    response = client.put("/competitions/LigaMx", json=updated_competition4)

    assert response.status_code == 200
    assert response.json()["id"] == 4
    assert response.json()["name"] == "LigaMx"
    assert response.json()["category"] == "amateur"
    assert response.json()["sport"] == "football"
    assert response.json()["teams"] == ["Mexico","Venecia"]



# Test para eliminar una competición (este con el id va y el anterior no... en fin)
def test_delete_competition():
    # Crear una competición para luego borrarla
    new_competition5 ={"id": 5, "name": "BBVA", "category": "professional", "sport": "football", "teams": ["Madrid", "Barça"]}
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




# Test para crear un match
def test_create_match():
    # Crear y añadir match
    new_macth2 = {'id': 2,
     'local': "UBSport",
     'visitor': 'UPC sport',
     'date': '2023-04-15',
     'price': 40.20}
    response = client.post("/matches/", json=new_macth2)
    assert response.status_code == 200
    assert response.json() == new_macth2

# Test de encontrar un match a traves de su id
def test_read_match_by_id():
    # Agregar match de prueba
    new_match ={'id': 1,
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
    # PROBLEMA: el servidor no puede entender la solicitud del
    # cliente debido a un error en la sintaxis o formato de los datos enviados.
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