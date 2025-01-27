FROM python:3.12-alpine3.21

RUN mkdir /app
RUN pip install poetry
COPY poetry.lock /app
COPY pyproject.toml /app

WORKDIR /app
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /app

CMD alembic upgrade head && python3 main.py