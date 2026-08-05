from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Portfolio
from analytics.lookthrough import compute_lookthrough_holdings
from analytics.kpis.returns import calculate_cagr, calculate_xirr
from datetime import date, timedelta

router = APIRouter()

@router.get("/portfolio")
def get_portfolio_summary(db: Session = Depends(get_db)):
    """Returns top-level portfolio valuation, return KPIs (XIRR, CAGR), and summary breakdown."""
    p = db.query(Portfolio).first()
    if not p:
        return {"error": "No portfolio found."}
        
    lookthrough = compute_lookthrough_holdings(db, p.portfolio_id)
    
    # Calculate mock cashflows for XIRR
    invested = lookthrough["total_invested"]
    curr_val = lookthrough["total_portfolio_value"]
    
    start_dt = date.today() - timedelta(days=365)
    cash_flows = [(start_dt, -invested), (date.today(), curr_val)]
    xirr_val = calculate_xirr(cash_flows)
    cagr_val = calculate_cagr(invested, curr_val, 1.0)
    
    return {
        "portfolio_id": p.portfolio_id,
        "name": p.name,
        "owner": p.owner,
        "total_value": curr_val,
        "total_invested": invested,
        "unrealized_gain": round(curr_val - invested, 2),
        "unrealized_gain_pct": round(((curr_val - invested) / invested * 100.0), 2) if invested > 0 else 0.0,
        "xirr": round(xirr_val, 2),
        "cagr": round(cagr_val, 2),
        "direct_assets_count": len(lookthrough["direct_assets"]),
        "underlying_stocks_count": len(lookthrough["lookthrough_stocks"]),
        "sector_breakdown": lookthrough["sector_breakdown"]
    }
