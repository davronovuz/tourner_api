from fastapi import FastAPI,Request
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.api.tournament import router as tournament_router
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



# DB connection (mos ravishda DB url-ni o'zgartiring)
DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/tournament_db_test"
engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI(title="Mini Tournament System")
app.include_router(tournament_router)




# Jinja2 templates papkasini konfiguratsiya qilish
templates = Jinja2Templates(directory="templates")

# Static fayllar uchun papkani ulash
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("tournament.html", {"request": request})




async def get_db():
    async with SessionLocal() as session:
        yield session


