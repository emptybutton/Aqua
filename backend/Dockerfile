FROM python:alpine

WORKDIR /aqua

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN apk add poetry && poetry env use /usr/local/bin/python && poetry install --no-root

CMD ["poetry", "run", "python", "-m", "uvicorn", "main:app", "--reload"]
