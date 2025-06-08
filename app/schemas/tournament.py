"""Pydantic schemas for tournament and player data."""

from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class TournamentCreate(BaseModel):
    """Schema for creating a new tournament."""

    name: str
    max_players: int



class TournamentResponse(BaseModel):
    """Schema for tournament response."""

    id: int
    name: str
    max_players: int
    start_at: datetime
    players: List["PlayerResponse"] = []

    class Config:
        orm_mode = True


class PlayerCreate(BaseModel):
    """Schema for creating a new player."""

    name: str
    email: EmailStr


class PlayerResponse(BaseModel):
    """Schema for player response."""

    id: int
    name: str
    email: EmailStr
    tournament_id: int

    class Config:
        """Configuration options for ORM mode."""
        from_attributes = True
