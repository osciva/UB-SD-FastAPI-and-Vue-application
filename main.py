from fastapi import FastAPI
from fastapi import HTTPException

import models
from models import Team

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



fake_teams_db = [{"team_name": "Barça"}, {"team_name": "Madrid"}, {"team_name": "Valencia"}]



@app.get("/teams/")
async def read_teams(skip: int = 0, limit: int = 10):
    return fake_teams_db[skip : skip + limit]

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
async def create_team(team: models.Team):
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
    team_index = next((index for (index, d) in enumerate(fake_teams_db) if d["team_name"] == team_name), None)
    if team_index is not None:
        del fake_teams_db[team_index]
        return {"message": f"{team_name} has been deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Team not found")



@app.put("/teams/{team_id}")
async def update_team(team_id: int, team: models.Team):
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
    existing_team = next(iter([x for x in fake_teams_db if x['team_name'] == team_name]), None)
    if not existing_team:
        # Si el equipo no existe, lo crea y lo añade a la lista
        new_team = {'team_name': team_name, 'name': team.name, 'country': team.country, 'description': team.description}
        fake_teams_db.append(new_team)
        return new_team
    else:
        # Si el equipo existe, actualiza los valores del equipo
        existing_team.update({'name': team.name, 'country': team.country, 'description': team.description})
        return existing_team
