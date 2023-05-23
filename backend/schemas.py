#mport enum
from backend.models import sports_list, categories_list, Category, Sports
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List




class TeamBase(BaseModel):
    name: str
    country: str
    description: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


class CompetitionBase(BaseModel):
    name: str
    category: Category
    sport: Sports



class CompetitionCreate(CompetitionBase):
    pass


class Competition(CompetitionBase):
    id: int
    teams: List[Team] = []
   # matches: List[Match] = []

    class Config:
        orm_mode = True


class MatchBase(BaseModel):
    date: datetime
    price: float
    """local: str
    visitor: str
    competition: str"""
    local: Team
    visitor: Team
    competition: Competition #Asi funciona con postman y como deberia ser
    total_available_tickets: int



class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    match_id: int
    tickets_bought: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    username: str

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    username: str
    password: str
    available_money: float
    is_admin: int
    orders: List[Order] = []


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):

    class Config:
        orm_mode = True









