from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routes import commodities, materials, rules, recommendation, report


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    from app.seed_data import main as seed_main
    seed_main()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Based Intelligent Food Packaging Material Recommendation System",
    lifespan=lifespan,
)

cors_origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(commodities.router)
app.include_router(materials.router)
app.include_router(rules.router)
app.include_router(recommendation.router)
app.include_router(report.router)


@app.get("/")
def root():
    return {"app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/api/health")
def health():
    return {"status": "ok"}
