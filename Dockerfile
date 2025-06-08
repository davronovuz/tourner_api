FROM python:3.11
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry install --only main
COPY . /app
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]