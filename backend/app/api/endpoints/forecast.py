from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Portfolio
from analytics.lookthrough import compute_lookthrough_holdings
from analytics.forecast import run_monte_carlo_simulation

router = APIRouter()

@router.get("/forecast")
def get_portfolio_forecast(
    horizon_years: int = Query(10, ge=1, le=30),
    monthly_sip: float = Query(10000.0, ge=0.0),
    target_goal: float = Query(5000000.0, ge=100000.0),
    db: Session = Depends(get_db)
):
    """Executes Monte Carlo simulation over specified horizon (5, 10, 15+ years) and returns percentiles."""
    p = db.query(Portfolio).first()
    curr_val = 800000.0
    if p:
        lt = compute_lookthrough_holdings(db, p.portfolio_id)
        curr_val = lt.get("total_portfolio_value", 800000.0)
        
    return run_monte_carlo_simulation(
        current_value=curr_val,
        monthly_sip=monthly_sip,
        expected_cagr=12.5,
        volatility=14.0,
        inflation_rate=6.0,
        horizon_years=horizon_years,
        target_goal=target_goal
    )
