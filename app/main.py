from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.limiter import limiter
from app.routes import auth, membros, financeiro, comunicacao, grupos, interessados
from app.database import engine, Base
import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Igreja Batista +500",
    version="1.0.0",
    description="Backend da plataforma Igreja Batista +500"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

cors_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(membros.router)
app.include_router(financeiro.router)
app.include_router(comunicacao.router)
app.include_router(grupos.router)
app.include_router(interessados.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "API Igreja Batista +500"}
