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

def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Match).offset(skip).limit(limit).all()

def get_match_by_id(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.id==match_id).first()

def get_matches_by_date(db: Session, date: str):
    return db.query(models.Match).filter(models.Match.date == date).all()


def create_match(db: Session, match: schemas.MatchCreate):
    db_match = models.Match(date=match.date,price=match.price,competition_id=match.competition_id,local_id=match.local_id,visitor_id=match.visitor_id)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

def get_competitions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Competition).offset(skip).limit(limit).all()

def get_competition_by_name(db: Session, name: str):
    return db.query(models.Competition).filter(models.Competition.name == name).first()

def get_competition_by_id(db: Session, competition_id: int):
    return db.query(models.Competition).filter(models.Competition.id == competition_id).first()

def create_competition(db: Session, competition: schemas.CompetitionCreate):
    db_competition = models.Competition(name=competition.name, category=competition.category, sport=competition.sport)
    db.add(db_competition)
    db.commit()
    db.refresh(db_competition)
    return db_competition
