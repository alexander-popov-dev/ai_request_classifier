FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main

COPY . .

CMD ["python", "-m", "src.main"]

