from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from models import Competition, Match, Team
from schemas import CompetitionCreate, MatchCreate, TeamCreate


# ----------------------------------------TEAMS----------------------------------------
def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def get_team_by_name(db: Session, name: str):
    print("Buscando equipo con nombre: ", name)
    team = db.query(models.Team).filter(models.Team.name == name).first()
    if team is None:
        print("No se encontró ningún equipo con el nombre: ", name)
    else:
        print("Se encontró el equipo: ", team.name)
    return team




def get_teams(db: Session, skip: int = 0, limit: int = 100):
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
    pass


def get_competitions_team(db: Session, team_name: str):
    pass


# ----------------------------------------COMPETITIONS----------------------------------------
def get_competition(db: Session, competition_id: int):
    return db.query(Competition).filter(Competition.id == competition_id).first()


def get_competition_by_name(db: Session, name: str):
    return db.query(Competition).filter(models.Competition.name == name).first()


def get_competitions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Competition).offset(skip).limit(limit).all()


def create_competition(db: Session, competition: Competition):
    db_competition = Competition(name=competition.name, category=competition.category, sport=competition.sport)
    for team_id in competition.teams:
        team = db.query(Team).filter(Team.id == team_id).first()
        db_competition.teams.append(team)
    #   for match_id in competition.matches:
    #       match = db.query(Match).filter(match.id == match_id).first()
    db.add(db_competition)
    db.commit()
    db.refresh(db_competition)
    return db_competition


def update_competition(db: Session, competition_id: int, competition: CompetitionCreate):
    db_competition = get_competition(db, competition_id)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    db_competition.name = competition.name
    db_competition.category = competition.category
    db_competition.sport = competition.sport
    db_competition.teams = []
    for team_id in competition.teams:
        team = get_team(db, team_id)
        if not team:
            raise HTTPException(status_code=404, detail=f"Team with id {team_id} not found")
        db_competition.teams.append(team)
    db.commit()
    db.refresh(db_competition)
    return db_competition


def delete_competition(db: Session, competition_id: int):
    db_competition = get_competition(db, competition_id)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    db.delete(db_competition)
    db.commit()
    return {"message": f"Competition with id {competition_id} has been deleted successfully."}


def get_matches_competition(db: Session, competition_name: str):
    pass


def get_teams_competition(db: Session, competition_name: str):
    pass

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
    print("Dentro de create_match")
    local_team = get_team_by_name(db, match.local)
    visitor_team = get_team_by_name(db, match.visitor)
    competition = get_competition_by_name(db, match.competition)
    print("despues de buscar competicion", competition.name, competition)
    """if competition is None:
        # Si la competición no existe, la creamos
        print("Creamos competicion")
        db_competition = Competition(name=match.competition, category="Senior", sport="Football")
        print("la competicion se hac reado bien", db_competition)
        db.add(db_competition)
        db.commit()
        db.refresh(db_competition)"""
    print("Definimos el match en la db")
    db_match = Match(date=match.date, price=match.price, competition=competition, local=local_team,
                     visitor=visitor_team)
    print("db_match creado", db_match.local)
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