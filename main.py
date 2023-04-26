
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


@app.get("/")
async def root():
    return {"message": "Hello World"}
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





#llegir les competicions
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





# Llegim els matches
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


# Actualitzem un match amb un cert id
@app.delete("/matches/{match_id}", response_model=schemas.Match)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match = repository.get_match(db, match_id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    repository.delete_match(db=db, match_id=match_id)
    return {"message": f"Match {match_id} has been deleted successfully."}

@app.put("/matches/{match_id}", response_model=schemas.Match)
def update_match(match_id: int, match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_match = repository.get_match(db=db, match_id=match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    updated_match = repository.update_match(db=db, match_id=match_id, match=match)
    return updated_match
