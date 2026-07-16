from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routes import router

app = FastAPI(
    title="Mello API",
    description="Assistente financeiro Mello",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def home():
    return RedirectResponse("/docs")