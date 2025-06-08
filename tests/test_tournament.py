"""Test suite for tournament API endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.models.tournament import Base

# Test configuration
TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:123@localhost:5432/tournament_db_test"
)

@pytest.fixture(scope="session")
def anyio_backend():
    """Configure the asyncio backend for anyio tests."""
    return "asyncio"

@pytest.fixture(scope="session")
async def engine():
    """Create and initialize the test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def session(engine):
    """Provide a database session for each test function."""
    session_local = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_local() as session:
        yield session
        await session.rollback()

@pytest.fixture(autouse=True)
def db_override(session):
    """Override the database dependency for test sessions."""
    async def get_db_override():
        yield session

    app.dependency_overrides[get_db] = get_db_override
    yield
    app.dependency_overrides.clear()

@pytest.mark.anyio
async def test_create_tournament():
    """Test the creation of a new tournament."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        tournament_data = {"name": "Test Cup", "max_players": 2}
        response = await client.post("/tournaments", json=tournament_data)
        assert response.status_code == 200  # noqa: S101
        data = response.json()
        assert data["name"] == "Test Cup"  # noqa: S101
        assert data["max_players"] == 2  # noqa: S101
        assert data["players"] == []  # noqa: S101

@pytest.mark.anyio
async def test_register_player():
    """Test registering a player for a tournament."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Create a tournament
        tournament_data = {"name": "Test Cup", "max_players": 2}
        response = await client.post("/tournaments", json=tournament_data)
        tournament_id = response.json()["id"]

        # Register a player
        player_data = {"name": "John Doe", "email": "john@example.com"}
        response = await client.post(
            f"/tournaments/{tournament_id}/register", json=player_data
        )
        assert response.status_code == 200  # noqa: S101
        assert response.json()["name"] == "John Doe"  # noqa: S101

        # Test duplicate email
        response = await client.post(
            f"/tournaments/{tournament_id}/register", json=player_data
        )
        assert response.status_code == 400  # noqa: S101
        assert "already registered" in response.json()["detail"]  # noqa: S101

        # Test tournament full
        player_data2 = {"name": "Jane Doe", "email": "jane@example.com"}
        response = await client.post(
            f"/tournaments/{tournament_id}/register", json=player_data2
        )
        assert response.status_code == 200  # noqa: S101
        player_data3 = {"name": "Bob Smith", "email": "bob@example.com"}
        response = await client.post(
            f"/tournaments/{tournament_id}/register", json=player_data3
        )
        assert response.status_code == 400  # noqa: S101
        assert "Tournament is full" in response.json()["detail"]  # noqa: S101

@pytest.mark.anyio
async def test_get_players():
    """Test retrieving players for a tournament."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        # Create a tournament
        tournament_data = {"name": "Test Cup", "max_players": 2}
        response = await client.post("/tournaments", json=tournament_data)
        tournament_id = response.json()["id"]

        # Register a player
        player_data = {"name": "John Doe", "email": "john@example.com"}
        await client.post(f"/tournaments/{tournament_id}/register", json=player_data)

        # Get players
        response = await client.get(f"/tournaments/{tournament_id}/players")
        assert response.status_code == 200  # noqa: S101
        players = response.json()
        assert isinstance(players, list)  # noqa: S101
        assert len(players) == 1  # noqa: S101
        assert players[0]["name"] == "John Doe"  # noqa: S101