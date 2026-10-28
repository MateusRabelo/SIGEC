import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.router import router
from app.services.mqtt_worker import run_mqtt_listener


@asynccontextmanager
async def lifespan(app: FastAPI):
    mqtt_task = asyncio.create_task(run_mqtt_listener())
    yield
    mqtt_task.cancel()
    try:
        await mqtt_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="SIGEC API",
    description="Sistema Inteligente de Gestão e Eficiência de Climatização",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)


if __name__ == "__main__":
    main()
