Mini Tournament System
This is a REST API for managing tournaments and registering players, built with FastAPI, SQLAlchemy, and PostgreSQL.
Features

Create a tournament (POST /tournaments)
Register a player to a tournament (POST /tournaments/{tournament_id}/register)
Get list of registered players (GET /tournaments/{tournament_id}/players)

Setup

Install Poetry:pip install poetry


Install dependencies:poetry install


Start PostgreSQL with Docker:docker-compose up -d


Run migrations:poetry run alembic upgrade head


Start the application:poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000



Testing
Run tests with pytest:
poetry run pytest

Linting and Formatting

Format code: poetry run black .
Check linting: poetry run ruff check .

API Documentation
Access Swagger UI at http://localhost:8000/docs after running the server.
