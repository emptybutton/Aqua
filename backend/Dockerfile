FROM python:alpine

WORKDIR /aqua

COPY . .

RUN apk add poetry && poetry install

CMD ["poetry", "run", "python", "-m", "uvicorn", "main:app", "--reload"]
