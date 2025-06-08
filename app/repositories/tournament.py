"""Repository layer for tournament data access."""

from app.models.tournament import Player, Tournament
from app.schemas.tournament import PlayerCreate, TournamentCreate
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List


class TournamentRepository:
    """Repository for managing tournament and player data."""

    def __init__(self, db: AsyncSession):
        """Initialize repository with database session."""
        self.db = db

    async def create_tournament(self, tournament: TournamentCreate) -> Tournament:
        """Create a new tournament with preloaded players."""
        db_tournament = Tournament(**tournament.model_dump())
        self.db.add(db_tournament)
        await self.db.commit()
        await self.db.refresh(
            db_tournament, {"players": selectinload(Tournament.players)}
        )
        return db_tournament

    async def register_player(self, tournament_id: int, player: PlayerCreate):
        """Register a player for a tournament."""
        tournament = await self.db.get(Tournament, tournament_id)
        if not tournament:
            raise HTTPException(status_code=404, detail="Tournament not found")
        current_players = await self.db.execute(
            select(Player).filter_by(tournament_id=tournament_id)
        )
        current_players = current_players.scalars().all()
        if len(current_players) >= tournament.max_players:
            raise HTTPException(status_code=400, detail="Tournament is full")
        existing_player = await self.db.execute(
            select(Player).filter_by(email=player.email, tournament_id=tournament_id)
        )
        if existing_player.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Player already registered")
        db_player = Player(
            name=player.name, email=player.email, tournament_id=tournament_id
        )
        self.db.add(db_player)
        try:
            await self.db.commit()
            await self.db.refresh(db_player)
            return db_player
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=400, detail="Email already exists"
            ) from None

    async def get_players(self, tournament_id: int) -> List[Player]:
        """Retrieve all players for a tournament."""
        result = await self.db.execute(
            select(Player).filter_by(tournament_id=tournament_id)
        )
        return result.scalars().all()