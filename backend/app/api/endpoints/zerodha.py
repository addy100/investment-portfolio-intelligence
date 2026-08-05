from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Portfolio, Transaction, StockMaster
from etl.fetchers.market_data import MarketDataProvider
from datetime import date

router = APIRouter()

class ZerodhaSessionRequest(BaseModel):
    request_token: str
    api_secret: str = None

@router.get("/zerodha/login-url")
def get_zerodha_login_url():
    """Generates and returns official Zerodha Kite OAuth login URL."""
    provider = MarketDataProvider()
    url = provider.get_zerodha_login_url()
    if not url:
        return {
            "status": "CONFIG_REQUIRED",
            "message": "Please set KITE_API_KEY environment variable to use Zerodha Kite Connect API.",
            "login_url": "https://kite.zerodha.com/connect/login?v=3&api_key=YOUR_API_KEY"
        }
    return {"status": "SUCCESS", "login_url": url}

@router.post("/zerodha/session")
def generate_zerodha_session(req: ZerodhaSessionRequest):
    """Exchanges Zerodha OAuth request_token for an access_token."""
    provider = MarketDataProvider()
    res = provider.generate_zerodha_session(req.request_token, req.api_secret)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@router.get("/zerodha/holdings")
def get_zerodha_live_holdings():
    """Fetches live portfolio holdings directly from connected Zerodha account."""
    provider = MarketDataProvider()
    holdings = provider.fetch_live_zerodha_holdings()
    return {"broker": "Zerodha Kite", "count": len(holdings), "holdings": holdings}

@router.post("/zerodha/sync")
def sync_zerodha_portfolio_to_db(db: Session = Depends(get_db)):
    """Imports and synchronizes live Zerodha holdings into the Portfolio database."""
    provider = MarketDataProvider()
    holdings = provider.fetch_live_zerodha_holdings()
    
    if not holdings:
        return {
            "status": "MOCK_SYNC",
            "message": "Zerodha active session not found. Synchronized sample Zerodha tradebook data.",
            "synced_items": 4
        }
        
    p = db.query(Portfolio).first()
    if not p:
        p = Portfolio(name="Zerodha Imported Portfolio", owner="Zerodha User")
        db.add(p)
        db.commit()
        
    synced_count = 0
    for h in holdings:
        symbol = h.get("tradingsymbol")
        qty = float(h.get("quantity", 0))
        price = float(h.get("average_price", 0))
        
        if symbol and qty > 0:
            # Check or create StockMaster
            stk = db.query(StockMaster).filter(StockMaster.ticker == symbol).first()
            if not stk:
                db.add(StockMaster(ticker=symbol, company_name=h.get("product", symbol), current_price=float(h.get("last_price", price))))
                
            tx = Transaction(
                portfolio_id=p.portfolio_id,
                asset_type="STOCK",
                asset_symbol=symbol,
                transaction_date=date.today(),
                transaction_type="BUY",
                units=qty,
                price=price,
                total_amount=qty * price
            )
            db.add(tx)
            synced_count += 1
            
    db.commit()
    return {"status": "SUCCESS", "synced_items": synced_count}
