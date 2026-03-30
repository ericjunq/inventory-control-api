from fastapi import FastAPI
from routers.auth_routers import auth_router
from routers.produtos_routers import produtos_router
from database import engine, Base
from routers.movimentacoes_routers import movimentacoes_router
from relatorio_routers import relatorio_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(produtos_router)
app.include_router(movimentacoes_router)
app.include_router(relatorio_router)

Base.metadata.create_all(bind=engine)
