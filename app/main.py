from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FC Career API",
    description="API REST para gestionar carreras de FC, equipos, temporadas y jugadores",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://fc-six-red.vercel.app",
        "https://fc-virid.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")