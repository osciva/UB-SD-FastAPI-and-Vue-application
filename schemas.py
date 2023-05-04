import enum
from models import sports_list, categories_list
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
    category: enum.Enum(*categories_list)
    sport: enum.Enum(*sports_list)



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
    local: Team
    visitor: Team
    competition: Competition


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True