from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, leaderboard, games

app = FastAPI(
    title="Snake Arena Online API",
    description="API for Snake Arena Online backend",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
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
