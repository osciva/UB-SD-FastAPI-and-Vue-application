from sqlalchemy.orm import Session
import models, schemas

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_team_by_name(db: Session, name: str):
    return db.query(models.Team).filter(models.Team.name == name).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(name=team.name, country=team.country, description=team.description)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team