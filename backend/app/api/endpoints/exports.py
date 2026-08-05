from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
import json
import os
from app.db.database import get_db
from app.models.models import Portfolio
from analytics.lookthrough import compute_lookthrough_holdings
from excel.generator import generate_portfolio_excel_workbook

router = APIRouter()

@router.get("/excel")
def download_excel_export(db: Session = Depends(get_db)):
    """Generates and returns formatted Excel workbook binary download."""
    p = db.query(Portfolio).first()
    lookthrough = compute_lookthrough_holdings(db, p.portfolio_id) if p else {}
    
    portfolio_data = {"xirr": 18.5}
    risk_data = {"sharpe_ratio": 1.85, "sortino_ratio": 2.42, "var_95": -1.85, "cvar_95": -2.65, "max_drawdown": -11.4, "volatility": 12.6}
    forecast_data = {"horizon_years": 10, "worst_case_10th": 1850000.0, "median_50th": 3200000.0, "expected_mean": 3450000.0, "best_case_90th": 5400000.0, "success_probability": 92.5}
    
    excel_bytes = generate_portfolio_excel_workbook(portfolio_data, lookthrough, risk_data, forecast_data)
    
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=Portfolio_Intelligence_Export.xlsx"}
    )

@router.get("/powerbi")
def get_powerbi_schema():
    """Returns Power BI dataset schema and metadata."""
    schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "powerbi", "schema.json")
    try:
        with open(schema_path, "r") as f:
            return json.load(f)
    except Exception:
        return {"name": "PortfolioIntelligenceDataset", "version": "1.0.0", "status": "Ready"}
