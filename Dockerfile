FROM python:3.12-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk update && apk add --no-cache curl \
    && rm -rf /var/cache/apk/*
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi

COPY . /app/

EXPOSE 8000
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
