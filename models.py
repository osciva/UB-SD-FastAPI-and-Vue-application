from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional


class Team(BaseModel):
    name: str
    country: str
    description: Optional[str] = None

