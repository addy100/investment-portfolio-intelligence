from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Portfolio
from analytics.lookthrough import compute_lookthrough_holdings

router = APIRouter()

@router.get("/holdings")
def get_portfolio_holdings(db: Session = Depends(get_db)):
    """Returns direct stock holdings + unravelled deep look-through stock exposures across funds."""
    p = db.query(Portfolio).first()
    if not p:
        return {"error": "No portfolio found."}
        
    return compute_lookthrough_holdings(db, p.portfolio_id)
