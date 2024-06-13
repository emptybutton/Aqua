FROM python:3.12-alpine3.19

WORKDIR /aqua

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH "/root/.local/bin:$PATH"

COPY pyproject.toml .
COPY poetry.lock .
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root

COPY . .

ENTRYPOINT ["poetry", "run"]
CMD ["ash"]
