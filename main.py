from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

import repository, models, schemas, utils
from schemas import SystemAccount
from database import SessionLocal, engine
from typing import List
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from utils import verify_password, create_access_token, create_refresh_token, get_hashed_password

# sessio5 imports
# from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from . import utils
from jose import jwt
from pydantic import ValidationError

from dependencies import get_settings, reuseable_oauth
from schemas import TokenPayload, SystemAccount
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend/dist/static"), name="static")

templates = Jinja2Templates(directory="frontend/dist")

models.Base.metadata.create_all(bind=engine)  # Creem la base de dades amb els models que hem definit a SQLAlchemy


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def get_current_user(settings: utils.Settings = Depends(get_settings),
                           db: Session = Depends(get_db),
                           token: str = Depends(reuseable_oauth)) -> SystemAccount:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.algorithm]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = token_data.sub
    # get user from database
    user = db.query(models.Account).filter(models.Account.username == username).first()
    # if user does not exist, raise an exception
    if not user:
        raise HTTPException(status_code = 400, detail = "User doesn't exist, use Sign In to create one")
    # if user exist, return user Schema with password hashed
    else:
        return SystemAccount(**user)


# ----------------------------------------TEAMS----------------------------------------
@app.get("/teams/", response_model=List[schemas.Team])
def read_teams(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_teams(db, skip=skip, limit=limit)


@app.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = repository.get_team_by_name(db, name=team.name)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already Exists, Use put for updating")
    else:
        return repository.create_team(db=db, team=team)


@app.get("/teams/{team_name}", response_model=schemas.Team)
def read_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.delete("/teams/{team_name}", response_model=dict)
def delete_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    repository.delete_team(db=db, team_name=team_name)
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


# retorna tots els partits d'un equip, donat el seu nom.
@app.get("/teams/{team_name}/matches", response_model=List[schemas.Match])
def get_matches_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    matches = repository.get_matches_team(db, team_name)
    return matches


# retorna totes les competicions d'un equip, donat el seu nom.
@app.get("/teams/{team_name}/competitions", response_model=schemas.Team)
def get_competitions_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    competitions = repository.get_competitions_team(db, team_name)
    return competitions


# ----------------------------------------COMPETITIONS----------------------------------------

# llegir les competicions
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


# actualitzar una competició amb un cert id
@app.put("/competitions/{competition_name}", response_model=schemas.Competition)
def update_competition(competition_name: str, competition: schemas.Competition, db: Session = Depends(get_db)):
    db_competition = repository.get_competition_by_name(db=db, name=competition_name)
    if not db_competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    updated_competition = repository.update_competition(db=db, competition_id=db_competition.id,
                                                        competition=competition)
    return updated_competition


# eliminar una competició amb un cert id
@app.delete("/competitions/{competition_name}", response_model=dict)
def delete_competition(competition_name: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, name=competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    repository.delete_competition(db=db, competition_id=competition.id)
    return {"message": f"{competition_name} has been deleted successfully."}


# retorna tots els partits d'una competició, donada el seu nom.
@app.get("/competitions/{competition_name}/matches", response_model=List[schemas.Competition])
def get_matches_competition(competition_name: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, name=competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    matches = repository.get_matches_competition(db=db, competition_name=competition.name)
    return matches


# retorna tots els equips d'una competició, donada el seu nom.
@app.get("/competitions/{competition_name}/teams", response_model=List[schemas.Competition])
def get_teams_competition(competition_name: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, name=competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    teams = repository.get_teams_competition(db=db, competition_name=competition.name)
    return teams


# ----------------------------------------MATCHES----------------------------------------

# Llegim els matches
@app.get("/matches/", response_model=List[schemas.Match])
def read_matches(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_matches(db, skip=skip, limit=limit)


"""@app.post("/matches/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    # En principio se pueden repetir nomrbes, deberiamos controlar, que no haya un mismo equipo jugando el mismo date
    db_match = repository.create_match(db=db, match=match)
    return db_match"""

"""@app.post("/matches/", response_model=schemas.Match)
=======

@app.post("/matches/", response_model=schemas.Match)
>>>>>>> 9680a673bfec7364bee0efeac63068ce73c8968e
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    # En principio se pueden repetir nomrbes, deberiamos controlar, que no haya un mismo equipo jugando el mismo date
    print("antes de llamarlo")
    db_match = repository.create_match(db=db, match=match)
    print("despues de llamarlo")

    return db_match"""


@app.post("/matches/", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    # Verificar que ambos equipos existen
    local_team = repository.get_team(db, match.local.id)
    if local_team is None:
        raise HTTPException(status_code=404, detail="Local team not found")

    visitor_team = repository.get_team(db, match.visitor.id)
    if visitor_team is None:
        raise HTTPException(status_code=404, detail="Visitor team not found")

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


# retorna l'equip local i visitant d'un partit, donat el seu id.
@app.get("/matches/{match_id}/teams", response_model=List[schemas.Match])
def get_teams_match(match_id: int, db: Session = Depends(get_db)):
    db_match = repository.get_match(db=db, match_id=match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    teams = repository.get_teams_match(db=db, match_id=match_id)
    return teams


# retorna la competició d'un partit, donat el seu id.
@app.get("/matches/{match_id}/competition", response_model=schemas.Competition)
def get_competition_match(match_id: int, db: Session = Depends(get_db)):
    db_match = repository.get_match(db=db, match_id=match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    competition = repository.get_competition_match()
    return competition


# ----------------------------------------ACCOUNTS Y ORDERS----------------------------------------
@app.get('/orders/{username}', response_model=List[schemas.Order])
def get_orders_by_username(username: str, db: Session = Depends(get_db)):
    orders = repository.get_orders_by_username(db, username=username)
    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return orders


# @app.post('/account', response_model=schemas.Account)
# def create_account(account: schemas.AccountCreate,db: Session = Depends(get_db)):
#     db_account = repository.get_account_by_username(db, username=account.username)
#     if db_account:
#         raise HTTPException(status_code=400, detail="Team already Exists, Use put for updating")
#     else:
#         return repository.create_account(db=db, account=account)
#


@app.post('/account', summary="Create new user", response_model=schemas.Account)
def create_user(data: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = repository.get_account_by_username(db, username=data.username)
    if db_account:
        raise HTTPException(status_code=404, detail="Account already exists, use PUT for updating")
    else:
        account_data = {
            'username': data.username,
            'password': get_hashed_password(data.password),
            'available_money': data.available_money,
            'is_admin': data.is_admin,
            'orders': data.orders
        }
        return repository.create_account(db=db, account=account_data)


@app.get('/orders', response_model=List[schemas.Order])
def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_orders(db, skip=skip, limit=limit)


@app.post('/orders/{username}', response_model=schemas.Order)
def create_orders_by_username(username: str, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # db_orders = repository.get_orders_by_username(db, username=username)
    # if db_orders:
    #     raise HTTPException(status_code=400, detail="Order already exists. Use PUT to update.")
    # else:
    return repository.create_orders(db=db, username=username, order=order)


@app.get('/accounts', response_model=List[schemas.Account])
def get_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # protegir endpoint
    # current_user = get_current_user(settings=Depends(get_settings()), db=db, token=Depends(reuseable_oauth))
    # if current_user.is_admin == 1:
    return repository.get_accounts(db, skip=skip, limit=limit)


@app.get('/account/{username}', response_model=schemas.Account)
def get_account_by_usename(username: str, db: Session = Depends(get_db)):
    account = repository.get_account_by_username(db, username=username)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.delete('/account/{username}', response_model=dict)
def delete_account(username: str, db: Session = Depends(get_db)):
    account = repository.get_account_by_username(db, username=username)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    repository.delete_account(db=db, username=username)
    return {"message": f"{account.username} has been deleted successfully."}


@app.put('/account/{username}', response_model=schemas.Account)
def update_account(username: str, acc: schemas.Account, db: Session = Depends(get_db)):
    account = repository.get_account_by_username(db=db, username=username)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    updated_account = repository.update_account(db=db, username=username, acc=acc)
    return updated_account


@app.post('/login', summary="Create access and refresh tokens for user", response_model=schemas.TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password
    # get user from database
    user = repository.get_account_by_username(db, username)
    # if user does not exist, raise an exception
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # if user exist, verify password using verify_password function
    else:
        pwd = verify_password(password, user.password)
        # pwd = verify_password(password, get_hashed_password(password))

        # if password is not correct, raise an exception
        if not pwd:
            raise HTTPException(status_code=400, detail="Incorrect Password")

        # if password is correct, create access and refresh tokens and return them
        else:
            return {
                "access_token": create_access_token(user.username),
                "refresh_token": create_refresh_token(user.username),
            }


@app.get('/account', summary='Get details of currently logged in user', response_model=SystemAccount)
def get_me(user: SystemAccount = Depends(get_current_user)):
    return user