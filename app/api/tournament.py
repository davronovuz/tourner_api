from fastapi import APIRouter, Depends, HTTPException
from app.services.tournament import TournamentService
from app.schemas.tournament import (
    TournamentCreate,
    TournamentResponse,
    PlayerCreate,
    PlayerResponse,
)
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

router = APIRouter()


"""API endpoints for tournament management."""

@router.post("/tournaments", response_model=TournamentResponse)
async def create_tournament(tournament: TournamentCreate, db: AsyncSession = Depends(get_db)):
    """Create a new tournament."""
    service = TournamentService(db)
    db_tournament = await service.create_tournament(tournament)
    return db_tournament


@router.post("/tournaments/{tournament_id}/register", response_model=PlayerResponse)
async def register_player(
    tournament_id: int, player: PlayerCreate, db: AsyncSession = Depends(get_db)
):
    service = TournamentService(db)
    return await service.register_player(tournament_id, player)


@router.get("/tournaments/{tournament_id}/players", response_model=List[PlayerResponse])
async def get_players(tournament_id: int, db: AsyncSession = Depends(get_db)):
    service = TournamentService(db)
    return await service.get_players(tournament_id)
