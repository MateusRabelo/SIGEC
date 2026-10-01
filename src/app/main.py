from fastapi import FastAPI
import uvicorn

from app.api.router import router

app = FastAPI(
    title="SIGEC API",
    description="Sistema Integrado de Gestao de Energia e Climatizacao",
    version="0.1.0",
)

app.include_router(router, prefix="/api")


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
