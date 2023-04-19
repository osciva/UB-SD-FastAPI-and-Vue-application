from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional, List


class Team(BaseModel):
    name: str
    country: str
    description: Optional[str] = None


class Competition(BaseModel):
    id: int
    name: str
    category: str
    sport: str
    teams: List

class Match(BaseModel):
    id: int
    local: str
    visitor: str
    date: str
    price: float
