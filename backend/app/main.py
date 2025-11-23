from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routers import auth, leaderboard, games
from app.database import init_db, _init_fake_data
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup: Initialize database
    print(f"Initializing database at: {settings.database_url}")
    init_db()
    print("✓ Database initialized")
    
    # Seed with fake data in debug mode
    if settings.debug:
        print("Debug mode: Seeding database with fake data...")
        _init_fake_data()
        print("✓ Fake data added")
    
    yield
    # Shutdown: cleanup if needed
    print("Shutting down...")


app = FastAPI(
    title="Snake Arena Online API",
    description="API for Snake Arena Online backend",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(leaderboard.router, prefix="/api")
app.include_router(games.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Snake Arena Online API"}
