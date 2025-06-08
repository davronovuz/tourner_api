"""Tournament service layer for business logic."""

from app.repositories.tournament import TournamentRepository
from app.schemas.tournament import TournamentCreate, PlayerCreate
from app.models.tournament import Tournament, Player


class TournamentService:
    """Service for managing tournament operations."""

    def __init__(self, db):
        """Initialize service with database session."""
        self.repository = TournamentRepository(db)

    async def create_tournament(self, tournament: TournamentCreate) -> Tournament:
        """Create a new tournament with preloaded players."""
        db_tournament = await self.repository.create_tournament(tournament)
        return db_tournament

    async def register_player(self, tournament_id: int, player: PlayerCreate) -> Player:
        """Register a player for a tournament."""
        return await self.repository.register_player(tournament_id, player)

    async def get_players(self, tournament_id: int) -> list[Player]:
        """Get all players registered in a tournament."""
        return await self.repository.get_players(tournament_id)
