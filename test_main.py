from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_team():
    # Creamos un equipo nuevo
    new_team = {"name": "Barcelona", "country": "Catalonia", "description": "Futbol Team"}
    response = client.post("/teams/", json=new_team)

    # Comprobamos que la respuesta es correcta
    assert response.status_code == 200
    assert response.json() == new_team


def test_delete_team():
    # Creamos un equipo nuevo
    new_team = {"name": "Barça", "country": "Catalonia", "description": "Futbol Team"}
    response = client.post("/teams/", json=new_team)

    # Comprobamos que la respuesta es correcta
    assert response.status_code == 200
    assert response.json() == new_team
    # eliminem al barça
    team_name = "Barça"
    response = client.delete(f"/teams/{team_name}")
    assert response.status_code == 200
    assert response.json() == {"message": f"{team_name} has been deleted successfully."}

    # comprovem que no estigui
    response = client.get("/teams/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert {"name": "Barça"} not in response.json()


def test_update_team():
    # Crear un equipo para actualizar
    client.post("/team", json={"name": "Real Madrid", "country": "Spain", "description": "The Kings of Europe"})
    # Actualizar el equipo con un nombre y una descripción diferentes
    response = client.put("/team/Real Madrid", json={"name": "Real Madrid CF", "country": "Spain", "description": "Hala Madrid!"})
    # Verificar que el equipo ha sido actualizado correctamente
    assert response.status_code == 200
    assert response.json()["name"] == "Real Madrid CF"
    assert response.json()["country"] == "Spain"
    assert response.json()["description"] == "Hala Madrid!"


# Test para obtener una competición por su nombre
def test_read_competition_by_name():
    # Agregar competición de prueba
    new_competition ={"id":1, "name": "SerieA", "category": "professional", "sport": "football", "teams": ["AC Milan", "Inter Milan"]}
    response = client.post("/competitions/", json=new_competition)
    assert response.status_code == 200
    assert response.json() == new_competition

    # Hacer petición GET
    response = client.get("/competitions/SerieA")


    # Verificar que la petición fue exitosa y que se obtuvo la competición correcta
    assert response.status_code == 200
    assert response.json() == new_competition

# Test para obtener una competición por su id
def test_read_competition_by_id():
    # Agregar competición de prueba
    new_competition2 ={"id": 2, "name": "BBVA", "category": "professional", "sport": "football", "teams": ["Madrid", "Barça"]}
    response = client.post("/competitions/", json=new_competition2)
    assert response.status_code == 200
    assert response.json() == new_competition2

    # Acceder a la competición creada
    response = client.get("/competitions/2")
    #PROBLEMA: no entiende el ID en la URL?
    assert response.status_code == 200
    assert response.json() == new_competition2


# Test para crear una competición
def test_create_competition():
    # Crear y añadir competición
    new_competition3 ={"id": 3, "name": "BBVA", "category": "professional", "sport": "football", "teams": ["Madrid", "Barça"]}
    response = client.post("/competitions/", json=new_competition3)
    assert response.status_code == 200
    assert response.json() == new_competition3


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
