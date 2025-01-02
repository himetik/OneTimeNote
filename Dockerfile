FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

RUN sphinx-build -b html documentation/source web/app/static/documentation

EXPOSE 8000

CMD sh -c "poetry run python3 -m web.app.database && poetry run gunicorn web.app.wsgi:app --bind 0.0.0.0:8000 --workers 3"
