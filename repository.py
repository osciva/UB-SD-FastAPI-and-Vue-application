from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from models import Competition, Match, Team
from schemas import CompetitionCreate, MatchCreate, TeamCreate


# ----------------------------------------TEAMS----------------------------------------
def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def get_team_by_name(db: Session, name: str):
    return db.query(models.Team).filter(models.Team.name == name).first()


def get_teams(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Team).offset(skip).limit(limit).all()


def create_team(db: Session, team: TeamCreate):
    db_team = models.Team(name=team.name, country=team.country, description=team.description)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def delete_team(db: Session, team_name: str):
    team = get_team_by_name(db, team_name)
    if not team:
        return None
    db.delete(team)
    db.commit()
    return team


def update_team(db: Session, team_name: str, team: TeamCreate):
    db_team = get_team_by_name(db, team_name)
    if not db_team:
        return None
    db_team.name = team.name
    db_team.country = team.country
    db_team.description = team.description
    db.commit()
    db.refresh(db_team)
    return db_team


def get_matches_team(db: Session, team_name: str):
    team = get_team_by_name(db, team_name)
    if not team:
        return None
    matches = get_matches(team)
    return matches


def get_competitions_team(db: Session, team_name: str):
    team = get_team_by_name(db, team_name)
    if not team:
        return None
    competitions = get_competitions(team)
    return competitions


# ----------------------------------------COMPETITIONS----------------------------------------
def get_competition(db: Session, competition_id: int):
    return db.query(Competition).filter(models.Competition.id == competition_id).first()


def get_competition_by_name(db: Session, name: str):
    return db.query(Competition).filter(models.Competition.name == name).first()


def get_competitions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Competition).offset(skip).limit(limit).all()


def create_competition(db: Session, competition: schemas.CompetitionCreate):
    db_competition = models.Competition(name=competition.name, category=competition.category, sport=competition.sport)

    #crear teams per a la competició
    for t in competition.teams:
        team_dict = t.dict()
        team_id = team_dict['id']
        team = db.query(models.Team).filter(models.Team.id == team_id).one()
        db_competition.teams.append(team)

    try:
        db.add(db_competition)
        db.commit()
        db.refresh(db_competition)
        return db_competition
    except:
        db.rollback()
        return "couldn't create the competition"


def update_competition(db: Session, competition_id: int, competition: Competition):
    db_competition = get_competition(db, competition_id)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    try:
        db_competition.name = competition.name
        db_competition.category = competition.category
        db_competition.sport = competition.sport
        db_competition.teams = []
        for team_id in competition.teams:
            team = get_team(db, team_id)
            if not team:
                raise HTTPException(status_code=404, detail=f"Team with id {team_id} not found")
            db_competition.teams.append(team)
        #for match_id in competition.matches:
         #   match = get_match(db, match_id)
          #  if not match:
           #     raise HTTPException(status_code=404, detail=f"match with id {match_id} not found")
            #db_competition.teams.append(match)
        db.commit()
        db.refresh(db_competition)
        return db_competition
    except:
        db.rollback()
        return {"message": "couldn't update the competition"}


def delete_competition(db: Session, competition_id: int):
    db_competition = get_competition(db, competition_id)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    try:
        db.delete(db_competition)
        db.commit()
        return {"message": f"Competition with id {competition_id} has been deleted successfully."}
    except:
        db.rollback()
        return {"message": "couldn't delete the competition"}

def get_matches_competition(db: Session, competition_name: str):
    db_competition = get_competition_by_name(db, competition_name)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    matches = get_matches(db_competition)
    return matches


def get_teams_competition(db: Session, competition_name: str):
    db_competition = get_competition_by_name(db, competition_name)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    teams = get_teams(db_competition)
    return teams

# ----------------------------------------MATCHES----------------------------------------
def get_match(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()


def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Match).offset(skip).limit(limit).all()


def get_match_by_id(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.id == match_id).first()


def get_matches_by_date(db: Session, date: str):
    return db.query(models.Match).filter(models.Match.date == date).all()


def create_match(db: Session, match: MatchCreate):
    db_match = Match(date=match.date, price=match.price, competition_id=match.competition_id, local_id=match.local_id,
                     visitor_id=match.visitor_id)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def delete_match(db: Session, match_id: int):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    db.delete(db_match)
    db.commit()
    return {"message": f"Match with id {match_id} has been deleted successfully."}


def update_match(db: Session, match_id: int, match: MatchCreate):
    db_match = get_match(db, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    db_match.date = match.date
    db_match.price = match.price
    db_match.competition_id = match.competition_id
    db_match.local_id = match.local_id
    db_match.visitor_id = match.visitor_id
    db.commit()
    db.refresh(db_match)
    return db_match

def get_teams_match(db: Session, match_id: int):
    pass


def get_competition_match(db: Session, match_id: int):
    pass