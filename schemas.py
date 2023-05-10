import enum
from models import sports_list, categories_list, Category, Sports
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



class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True

