
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import repository, models, schemas
from database import SessionLocal, engine
from typing import List




models.Base.metadata.create_all(bind=engine) # Creem la base de dades amb els models que hem definit a SQLAlchemy

app = FastAPI()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/teams/", response_model=List[schemas.Team])
def read_teams(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_teams(db, skip=skip, limit=limit)

@app.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate,db: Session = Depends(get_db)):
    db_team = repository.get_team_by_name(db, name=team.name)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already Exists, Use put for updating")
    else:
        return repository.create_team(db=db, team=team)

@app.get("/team/{team_name}", response_model=schemas.Team)
def read_team(team_name: str,db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.get("/competitions/", response_model=List[schemas.Competition])
def read_competitions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_competitions(db, skip=skip, limit=limit)


@app.post("/competitions/", response_model=schemas.Competition)
def create_competition(competition: schemas.CompetitionCreate, db: Session = Depends(get_db)):
    db_competition = repository.get_competition_by_name(db, name=competition.name)
    if db_competition:
        raise HTTPException(status_code=400, detail="Competition already exists, use PUT for updating")
    else:
        return repository.create_competition(db=db, competition=competition)

@app.get("/competition/{competition_name}", response_model=schemas.Competition)
def read_competition_by_name(competition_name: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, name=competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return competition

@app.get("/competitions/{competition_id}", response_model=schemas.Competition)
def read_competition_by_id(competition_id: int, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_id(db, competition_id=competition_id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return competition


@app.get("/matches/", response_model=List[schemas.Match])
def read_matches(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_matches(db, skip=skip, limit=limit)


@app.post("/matches/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    # En principio se pueden repetir nomrbes, deberiamos controlar, que no haya un mismo equipo jugando el mismo date
    db_match = repository.create_match(db=db, match=match)
    return db_match

@app.get("/matches/{match_id}", response_model=schemas.Match)
def read_match_by_id(match_id: int, db: Session = Depends(get_db)):
    match = repository.get_match_by_id(db, match_id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@app.get("/matches/{match_date}", response_model=List[schemas.Match])
def read_matches_by_date(date: str, db: Session = Depends(get_db)):
    matches = repository.get_matches_by_date(db, date=date)
    if not matches:
        raise HTTPException(status_code=404, detail="No matches found for this date")
    return matches



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




@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}



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
async def update_team(team_id: int, team: schemas.Team):
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
async def update_team(team_name: str, team: schemas.Team):
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
async def create_competition(competition: schemas.Competition):

    fake_competitions_db.append(competition)
    return competition

#actualitzar una competició amb un cert id
@app.put("/competitions/{competition_name}")
async def update_competition(competition_name: str, competition: schemas.Competition):
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


fake_matches_db = []

# Llegim els matches
@app.get("/matches/")
async def read_matches(skip: int = 0, limit: int = 10):
    return fake_matches_db[skip: skip + limit]

# Obtenim un match amb un cert id
@app.get("/matches/{match_id}")
async def read_match(match_id: int):
    match = next((mat for mat in fake_matches_db if mat.id == match_id), None)
    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

# Creem un match
@app.post("/matches/")
async def create_match(match: schemas.Match):
    fake_matches_db.append(match)
    return match

# Actualitzem un match amb un cert id
@app.put("/matches/{match_id}")
async def update_match(match_id: int, match: schemas.Match):
    for i, m in enumerate(fake_matches_db):
        if m.id == match_id:
            fake_matches_db[i] = match
            return match
    raise HTTPException(status_code=404, detail="Match not found")


#eliminar una competició amb un cert id
@app.delete("/matches/{match_id}")
async def delete_match(match_id: int):
    global fake_matches_db
    match_index = next((index for (index, c) in enumerate(fake_matches_db) if c.id == match_id), None)
    if match_index is None:
        raise HTTPException(status_code=404, detail="Match not found")
    del fake_matches_db[match_index]
    return {"message": f"{match_id} has been deleted successfully."}
