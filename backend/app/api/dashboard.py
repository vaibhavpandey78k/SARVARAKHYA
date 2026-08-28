from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.analytics_service import overview, rankings, rules, precursors

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/overview")
def get_overview(db: Session = Depends(get_db)): return overview(db)

@router.get("/sites")
def get_sites(db: Session = Depends(get_db)): return rankings(db, "site")

@router.get("/activities")
def get_activities(db: Session = Depends(get_db)): return rankings(db, "activity")

@router.get("/rules")
def get_rules(db: Session = Depends(get_db)): return rules(db)

@router.get("/precursors")
def get_precursors(db: Session = Depends(get_db)): return precursors(db)
