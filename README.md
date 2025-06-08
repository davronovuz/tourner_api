# 🏆 Mini Tournament System

REST API for managing tournaments and registering players, built with **FastAPI**, **SQLAlchemy 2.0+**, and **PostgreSQL**.

---

## 🚀 Features

- **Create a tournament**  
  `POST /tournaments`  
  Create a new tournament with name, max players, and start date.

- **Register a player**  
  `POST /tournaments/{tournament_id}/register`  
  Register a player for a tournament by name and email.  
  Constraints:
  - The number of registered players cannot exceed the tournament’s limit.
  - The same email cannot be registered twice in one tournament.

- **List registered players**  
  `GET /tournaments/{tournament_id}/players`  
  Get the list of players registered in a tournament.

- **Validation & Error Handling**  
  Pydantic validation, proper error codes (422, 400, etc).

- **Async support**  
  All endpoints are fully async.

- **Database migrations**  
  Managed via Alembic.

- **Testing, linting, formatting**  
  All code is type-checked, formatted, and covered by at least one test.

---

## ⚙️ Tech Stack

- Python 3.11+
- FastAPI
- Async SQLAlchemy 2.0+
- Alembic (migrations)
- Pydantic
- PostgreSQL
- Docker & Docker Compose
- Poetry (dependency management)
- Mypy, Ruff, Black
- Pytest

---

## 🛠️ Setup & Usage

### 1. Install Poetry (if not installed)
```bash
pip install poetry
```

### 2. Install dependencies
```bash
poetry install
```

### 3. Start PostgreSQL with Docker
```bash
docker-compose up -d
```

### 4. Run migrations
```bash
poetry run alembic upgrade head
```

### 5. Start the application
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## ✅ Testing

Run all tests with:
```bash
poetry run pytest
```

---

## 🧹 Linting & Formatting

- **Format code:**  
  ```bash
  poetry run black .
  ```

- **Check linting:**  
  ```bash
  poetry run ruff check .
  ```

- **Type checking:**  
  ```bash
  poetry run mypy .
  ```

---

## 📚 API Documentation

Interactive Swagger UI is available at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📦 Project Structure

```
project/
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── api/
│   ├── templates/
│   ├── db.py
│   └── config.py
├── alembic/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## 📄 License

MIT

---

**Happy coding!**