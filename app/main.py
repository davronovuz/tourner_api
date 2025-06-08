from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.api.tournament import router as tournament_router

# DB connection (mos ravishda DB url-ni o'zgartiring)
DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/tournament_db_test"
engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI(title="Mini Tournament System")
app.include_router(tournament_router)

# --- Bu funksiya testlar uchun ham, ilova uchun ham kerak ---
async def get_db():
    async with SessionLocal() as session:
        yield session