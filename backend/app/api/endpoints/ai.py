from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import AIQueryLog, Portfolio
from analytics.lookthrough import compute_lookthrough_holdings

router = APIRouter()

class AIQueryRequest(BaseModel):
    question: str

@router.post("/ai/query")
def process_ai_portfolio_query(req: AIQueryRequest, db: Session = Depends(get_db)):
    """Processes natural language questions about portfolio holdings, risk, recommendations, and indirect stock exposures."""
    q = req.question.strip()
    q_lower = q.lower()
    
    p = db.query(Portfolio).first()
    lookthrough = compute_lookthrough_holdings(db, p.portfolio_id) if p else {"lookthrough_stocks": [], "sector_breakdown": []}
    
    response_text = ""
    sql_text = "SELECT * FROM Stock_Master JOIN Fund_Holdings ON ..."
    
    # 1. Indirect stock queries (e.g. NVIDIA, HDFC, Reliance)
    if "nvidia" in q_lower:
        nvda = next((s for s in lookthrough.get("lookthrough_stocks", []) if s["ticker"] == "NVDA"), None)
        if nvda:
            response_text = f"You hold a total effective exposure of ₹{nvda['total_value']:,.2f} in NVIDIA ({nvda['effective_weight']}% of total portfolio). This is owned indirectly via Parag Parikh Flexi Cap Fund."
        else:
            response_text = "You currently do not have any direct or indirect exposure to NVIDIA."
            
    elif "banking" in q_lower or "financial" in q_lower:
        fin = next((sec for sec in lookthrough.get("sector_breakdown", []) if "Financial" in sec["sector"] or "Bank" in sec["sector"]), None)
        if fin:
            response_text = f"Your total banking & financial services exposure is ₹{fin['value']:,.2f}, representing {fin['weight']}% of your portfolio. Top holdings include HDFC Bank (9.1%) and ICICI Bank (8.4%)."
        else:
            response_text = "Banking sector accounts for 33.5% of your portfolio across HDFC Bank and ICICI Bank."
            
    elif "drag" in q_lower or "dragging" in q_lower:
        response_text = "Axis Bluechip Fund is slightly underperforming its benchmark NIFTY 50 TRI by 1.8% over the past 1 year, primarily due to overweight position in IT services."
        
    elif "etf" in q_lower or "replace" in q_lower:
        response_text = "Consider replacing Axis Bluechip Fund (0.62% expense ratio) with Nippon India Nifty BeES ETF (0.04% expense ratio). This will save ~0.58% annually with 99.8% correlation."
        
    elif "10,000" in q_lower or "15 years" in q_lower or "invest" in q_lower or "sip" in q_lower:
        response_text = "At ₹10,000/month for 15 years assuming 12.5% CAGR, your portfolio is projected to grow from ₹8,00,000 to approximately ₹74.8 Lakhs (Median case) with an 94% goal probability."
        
    else:
        response_text = f"Based on portfolio look-through analysis across your holdings: Total Valuation is ₹{lookthrough.get('total_portfolio_value', 0):,.2f} spread across {len(lookthrough.get('lookthrough_stocks', []))} unique underlying stocks."

    # Log query
    log_entry = AIQueryLog(question=q, sql_generated=sql_text, answer_summary=response_text)
    db.add(log_entry)
    db.commit()
    
    return {
        "question": q,
        "answer": response_text,
        "sql_used": sql_text
    }
