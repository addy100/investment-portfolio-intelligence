from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import FundMaster
from analytics.overlap import compute_portfolio_overlap_matrix, calculate_hhi_and_effective_stocks
from analytics.lookthrough import compute_lookthrough_holdings
from app.models.models import Portfolio

router = APIRouter()

@router.get("/overlap")
def get_portfolio_overlap(db: Session = Depends(get_db)):
    """Returns pairwise fund overlap matrix, common stock holdings, and HHI concentration index."""
    funds = db.query(FundMaster).all()
    scheme_codes = [f.scheme_code for f in funds if f.scheme_code != "NIFTYBEES"]
    
    overlap_data = compute_portfolio_overlap_matrix(db, scheme_codes)
    
    p = db.query(Portfolio).first()
    lookthrough = compute_lookthrough_holdings(db, p.portfolio_id) if p else {"lookthrough_stocks": []}
    
    weights = [s["effective_weight"] for s in lookthrough.get("lookthrough_stocks", [])]
    hhi_data = calculate_hhi_and_effective_stocks(weights)
    
    return {
        "funds": overlap_data["funds"],
        "matrix": overlap_data["matrix"],
        "pairwise_details": overlap_data["pairwise_details"],
        "hhi_index": hhi_data["hhi"],
        "effective_num_stocks": hhi_data["effective_num_stocks"]
    }
