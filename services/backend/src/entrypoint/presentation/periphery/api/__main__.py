import uvicorn

from entrypoint.presentation.periphery.api.apps import app


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104


if __name__ == "__main__":
    main()
