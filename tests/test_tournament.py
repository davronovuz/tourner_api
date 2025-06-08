import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app,get_db
from app.models.tournament import Base

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/tournament_db_test"

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def session(engine):
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture(autouse=True)
def _db_override(session):
    async def _get_db_override():
        yield session
    app.dependency_overrides[get_db] = _get_db_override
    yield
    app.dependency_overrides.clear()

@pytest.mark.anyio
async def test_create_tournament():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        tournament_data = {
            "name": "Test Cup",
            "max_players": 2,
        }
        response = await client.post("/tournaments", json=tournament_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Cup"
        assert data["max_players"] == 2
        assert data["players"] == []

@pytest.mark.anyio
async def test_register_player():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        tournament_data = {
            "name": "Test Cup",
            "max_players": 2,
        }
        response = await client.post("/tournaments", json=tournament_data)
        tournament_id = response.json()["id"]

        player_data = {"name": "John Doe", "email": "john@example.com"}
        response = await client.post(f"/tournaments/{tournament_id}/register", json=player_data)
        assert response.status_code == 200
        assert response.json()["name"] == "John Doe"

        # Test duplicate email
        response = await client.post(f"/tournaments/{tournament_id}/register", json=player_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

        # Test tournament full
        player_data2 = {"name": "Jane Doe", "email": "jane@example.com"}
        response = await client.post(f"/tournaments/{tournament_id}/register", json=player_data2)
        assert response.status_code == 200
        player_data3 = {"name": "Bob Smith", "email": "bob@example.com"}
        response = await client.post(f"/tournaments/{tournament_id}/register", json=player_data3)
        assert response.status_code == 400
        assert "Tournament is full" in response.json()["detail"]

@pytest.mark.anyio
async def test_get_players():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        tournament_data = {
            "name": "Test Cup",
            "max_players": 2,
        }
        response = await client.post("/tournaments", json=tournament_data)
        tournament_id = response.json()["id"]

        player_data = {"name": "John Doe", "email": "john@example.com"}
        await client.post(f"/tournaments/{tournament_id}/register", json=player_data)

        response = await client.get(f"/tournaments/{tournament_id}/players")
        assert response.status_code == 200
        players = response.json()
        assert isinstance(players, list)
        assert len(players) == 1
        assert players[0]["name"] == "John Doe"