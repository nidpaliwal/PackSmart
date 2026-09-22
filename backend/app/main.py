from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routes import commodities, materials, rules, recommendation, report

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Based Intelligent Food Packaging Material Recommendation System",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(commodities.router)
app.include_router(materials.router)
app.include_router(rules.router)
app.include_router(recommendation.router)
app.include_router(report.router)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/api/health")
def health():
    return {"status": "ok"}
