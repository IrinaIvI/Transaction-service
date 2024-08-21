FROM debian:bookworm-slim

LABEL maintainer="ira.ivashko.99@gmail.com"

# WORKDIR /app
WORKDIR /app

ENV POETRY_VERSION=1.8.3
ENV PATH="/root/.local/bin:${PATH}"


# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    postgresql-client \
    libpq-dev && \
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 - && \
    /root/.local/bin/poetry --version

# # Установка системных зависимостей
# RUN apt-get update && \
#     apt-get install -y python3 python3-pip python3-venv curl && \
#     curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 - && \
#     /root/.local/bin/poetry --version

RUN poetry config virtualenvs.create true

COPY ./transactions/poetry.lock ./transactions/pyproject.toml /app/
RUN poetry install --no-interaction --no-ansi

# Копирование исходного кода
COPY ./transactions/src /app/src
COPY ./common_base.py /app/common_base.py

ENV PYTHONPATH=/app/src

ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
