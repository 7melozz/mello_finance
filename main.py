from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routes_users import router as users_router
from app.api.routes_accounts import router as accounts_router
from app.api.routes_transactions import router as transactions_router
from app.api.routes_categories import router as categories_router

app = FastAPI(
    title="Mello API",
    description="API financeira pessoal com arquitetura limpa e evolução para V1.5.",
    version="1.5.0",
)

app.include_router(users_router)
app.include_router(accounts_router)
app.include_router(transactions_router)
app.include_router(categories_router)

@app.get("/")
def home():
    return RedirectResponse("/docs")