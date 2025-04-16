FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /uvx /bin/

COPY ./uv.lock .
COPY ./pyproject.toml .
RUN uv sync --frozen

RUN uv run playwright install

COPY ./backend backend

EXPOSE 8000

CMD ["uv", "run", "./backend/app/main.py"]