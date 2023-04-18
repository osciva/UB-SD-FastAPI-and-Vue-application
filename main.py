from fastapi import FastAPI
from fastapi import HTTPException

import models
from models import Team
from models import Competition

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/python')
def like_python():
    return {'I like Python!'}


fake_teams_db = []


@app.get("/teams/")
async def read_teams(skip: int = 0, limit: int = 10):
    return fake_teams_db[skip: skip + limit]


@app.get("/team/{team_name}")
async def read_team(team_name: str):
    team = next(iter([x for x in fake_teams_db if x["team_name"] == team_name]), None)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return {'team': team_name}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.post("/teams/")
async def create_team(team: Team):
    if not fake_teams_db:
        fake_teams_db.append(team)
    else:
        exists_team = next(iter([x for x in fake_teams_db if x.name == team.name]), None)
        if not exists_team:
            fake_teams_db.append(team)
        else:
            raise HTTPException(status_code=404, detail="Team already Exists, Use put for updating")
    return team


@app.delete("/teams/{team_name}")
async def delete_team(team_name: str):
    global fake_teams_db
    team_index = next((index for (index, team) in enumerate(fake_teams_db) if team.name == team_name), None)


    if team_index is not None:
        del fake_teams_db[team_index]
        return {"message": f"{team_name} has been deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Team not found")


@app.put("/teams/{team_id}")
async def update_team(team_id: int, team: Team):
    if not fake_teams_db:
        fake_teams_db.append(team)
        return team
    else:
        for idx, t in enumerate(fake_teams_db):
            if t.id == team_id:
                fake_teams_db[idx] = team
                return team
        else:
            fake_teams_db.append(team)
            return team


@app.put("/team/{team_name}")
async def update_team(team_name: str, team: models.Team):
    existing_team = next(iter([x for x in fake_teams_db if x.name == team_name]), None)

    if not existing_team:
        # Si el equipo no existe, lo crea y lo añade a la lista
        new_team = {'team_name': team_name, 'name': team.name, 'country': team.country, 'description': team.description}
        fake_teams_db.append(new_team)
        return new_team
    else:
        # Si el equipo existe, actualiza los valores del equipo
        existing_team.update({'name': team.name, 'country': team.country, 'description': team.description})
        return existing_team

fake_competitions_db = []


#llegir les competicions
@app.get("/competitions/")
async def read_competitions(skip: int = 0, limit: int = 10):
    return fake_competitions_db[skip: skip + limit]

#obtenir una competició amb un cert nom (no crec que fagi falta però a l'enunciat no ho deixa clar)
#@app.get("/competitions/{competition_name}")
#async def read_competition(competition_name: str):
    #competition = next(iter([x for x in fake_competitions_db if x.name == competition_name]), None)
    #if not competition:
        #raise HTTPException(status_code=404, detail="Competition not found")
    #return competition


#obtenir una competició amb un cert id
@app.get("/competitions/{competition_id}")
async def read_competition(competition_id: int):
    competition = next((comp for comp in fake_competitions_db if comp.id == competition_id), None)
    if competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    return competition

#crear una competició
@app.post("/competitions/")
async def create_competition(competition: Competition):

    fake_competitions_db.append(competition)
    return competition

#actualitzar una competició amb un cert id
@app.put("/competitions/{competition_name}")
async def update_competition(competition_name: str, competition: Competition):
    competition_index = next((index for (index, c) in enumerate(fake_competitions_db) if c.name == competition_name), None)
    if competition_index is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    fake_competitions_db[competition_index] = competition
    return competition

#eliminar una competició amb un cert id
@app.delete("/competitions/{competition_id}")
async def delete_competition(competition_id: int):
    global fake_competitions_db
    competition_index = next((index for (index, c) in enumerate(fake_competitions_db) if c.id == competition_id), None)
    if competition_index is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    del fake_competitions_db[competition_index]
    return {"message": f"{competition_id} has been deleted successfully."}
