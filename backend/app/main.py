"""
RuralBiz Navigator - FastAPI Application Entrypoint
SIH 2026 Problem Statement SIH26091 / PS 91
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import PROJECT_NAME, VERSION, API_V1_PREFIX, CORS_ORIGINS
from backend.app.api.router import api_router

app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description="AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware for Next.js Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS + ["*"], # Allow all during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 Router
app.include_router(api_router, prefix=API_V1_PREFIX)

@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "app": PROJECT_NAME,
        "version": VERSION,
        "docs": "/docs",
        "api_v1": API_V1_PREFIX
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

