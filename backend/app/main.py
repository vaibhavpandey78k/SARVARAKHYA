from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.models import Report, Prediction, HumanReview  # noqa: F401
from app.api.reports import router as reports_router
from app.api.dashboard import router as dashboard_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_list or ["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(reports_router)
app.include_router(dashboard_router)

@app.get("/health", tags=["System"])
def health():
    return {"status": "ok", "service": settings.app_name, "model_version": settings.model_version}
