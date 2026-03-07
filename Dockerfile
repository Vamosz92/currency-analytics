FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y curl build-essential libpq-dev

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . /app