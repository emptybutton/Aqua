FROM python:alpine

WORKDIR /aqua

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN apk add poetry && poetry install --no-root

ENTRYPOINT ["poetry", "run"]
CMD ["ash"]
