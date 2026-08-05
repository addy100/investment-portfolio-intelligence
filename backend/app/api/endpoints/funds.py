from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import FundMaster, FundNAV, FundHoldings

router = APIRouter()

@router.get("/funds")
def get_funds_list(db: Session = Depends(get_db)):
    """Returns list of all mutual funds and ETFs in fund master with expense ratios and category info."""
    funds = db.query(FundMaster).all()
    results = []
    for f in funds:
        latest_nav = db.query(FundNAV).filter(FundNAV.scheme_code == f.scheme_code).order_by(FundNAV.nav_date.desc()).first()
        holdings_count = db.query(FundHoldings).filter(FundHoldings.scheme_code == f.scheme_code).count()
        
        results.append({
            "scheme_code": f.scheme_code,
            "fund_name": f.fund_name,
            "amc": f.amc,
            "category": f.category,
            "sub_category": f.sub_category,
            "expense_ratio": f.expense_ratio,
            "turnover_ratio": f.turnover_ratio,
            "benchmark_index": f.benchmark_index,
            "latest_nav": latest_nav.nav if latest_nav else None,
            "holdings_count": holdings_count
        })
        
    return {"funds": results}
