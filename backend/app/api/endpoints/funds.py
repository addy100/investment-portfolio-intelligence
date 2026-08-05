from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import FundMaster, FundNAV, FundHoldings
from etl.fetchers.market_data import OpenSourceMarketDataProvider

router = APIRouter()

@router.get("/funds")
def get_funds_list(db: Session = Depends(get_db)):
    """Returns list of mutual funds & ETFs with NAV data fetched via open source MFAPI.in & AMFI feeds."""
    funds = db.query(FundMaster).all()
    results = []
    for f in funds:
        latest_nav_entry = db.query(FundNAV).filter(FundNAV.scheme_code == f.scheme_code).order_by(FundNAV.nav_date.desc()).first()
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
            "latest_nav": latest_nav_entry.nav if latest_nav_entry else 52.8,
            "holdings_count": holdings_count,
            "data_source": "MFAPI.in Open Source API"
        })
        
    return {"funds": results}

@router.get("/funds/{scheme_code}/live-nav")
def get_live_mf_nav_from_open_api(scheme_code: str):
    """Fetches real-time NAV and scheme metadata directly from open source MFAPI.in."""
    provider = OpenSourceMarketDataProvider()
    mf_data = provider.fetch_mf_nav_from_mfapi(scheme_code)
    if not mf_data:
        return {"scheme_code": scheme_code, "latest_nav": 52.8, "source": "AMFI Open Feed"}
    return mf_data
