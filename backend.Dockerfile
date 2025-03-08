FROM python:3.12-slim-bookworm

WORKDIR /usr/src/app

COPY --from=ghcr.io/astral-sh/uv:0.6.5 /uv /uvx /bin/

COPY ./uv.lock .
COPY ./pyproject.toml .
RUN uv sync --frozen

RUN uv run playwright install

COPY ./backend backend

EXPOSE 8000

CMD ["uv", "run", "./backend/app/main.py"]