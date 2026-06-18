from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, membros, financeiro, comunicacao

app = FastAPI(
    title="API Igreja Batista +500",
    version="1.0.0",
    description="Backend da plataforma Igreja Batista +500"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(membros.router)
app.include_router(financeiro.router)
app.include_router(comunicacao.router)

@app.get("/")
def root():
    return {"status": "ok", "message": "API Igreja Batista +500"}
