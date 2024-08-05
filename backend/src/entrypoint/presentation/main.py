from fastapi import FastAPI

from entrypoint.presentation.routes import router


app = FastAPI()
app.include_router(router)
