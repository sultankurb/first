FROM python:3.12-alpine3.21

RUN mkdir /app
RUN pip install poetry
COPY poetry.lock /app
COPY pyproject.toml /app

RUN cd /app
RUN poetry install
COPY . /app

CMD["cd /app/scripts", "&&", "./start.sh"]