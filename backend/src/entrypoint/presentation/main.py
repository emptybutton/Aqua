from fastapi import FastAPI

from src.entrypoint.presentation.routes import router


app = FastAPI()
app.include_router(router)
