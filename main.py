
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





@app.delete("/teams/{team_name}", response_model=schemas.Team)
def delete_team(team_name: str, team: schemas.Team, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team.name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    repository.delete_team(db=db,team_name=team.name)
    return {"message": f"{team_name} has been deleted successfully."}

@app.put("/teams/{team_id}", response_model=schemas.Team)
def update_team(team_id: int, team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = repository.get_team(db=db, team_id=team_id)
    if not db_team:
        db_team = repository.create_team(db=db, team=team)
    else:
        db_team = repository.update_team(db=db, team_name=db_team.name, team=team)
    return db_team

@app.put("/team/{team_name}", response_model=schemas.Team)
def update_team_by_name(team_name: str, team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = repository.get_team_by_name(db=db, name=team_name)
    if not db_team:
        db_team = repository.create_team(db=db, team=team)
    else:
        db_team = repository.update_team(db=db, team_name=db_team.name, team=team)
    return db_team


fake_competitions_db = []


#llegir les competicions
@app.get("/competitions/", response_model=schemas.Competition)
def read_competitions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_competitions(db, skip=skip, limit=limit)

@app.post("/competitions/", response_model=schemas.Competition)
def create_competition(competition: schemas.CompetitionCreate, db: Session = Depends(get_db)):
    return repository.create_competition(db=db, competition=competition)

@app.get("/competitions/{competition_id}", response_model=schemas.Competition)
def read_competition(competition_id: int, db: Session = Depends(get_db)):
    db_competition = repository.get_competition(db, competition_id=competition_id)
    if db_competition is None:
        raise HTTPException(status_code=404, detail="Competition not found")
    return db_competition

#actualitzar una competició amb un cert id
@app.put("/competitions/{competition_name}", response_model=schemas.Competition)
def update_competition(competition_name: str, competition: schemas.CompetitionCreate, db: Session = Depends(get_db)):
    db_competition = repository.get_competition_by_name(db=db, name=competition_name)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    updated_competition = repository.update_competition(db=db, competition_id=db_competition.id, competition=competition)
    return updated_competition


#eliminar una competició amb un cert id
@app.delete("/competitions/{competition_name}", response_model=schemas.Competition)
def delete_competition(competition_name: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, name=competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    repository.delete_competition(db=db, competition_id=competition.id)
    return {"message": f"{competition_name} has been deleted successfully."}



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
