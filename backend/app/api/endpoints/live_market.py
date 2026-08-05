from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.models import StockMaster, PriceHistory
from etl.fetchers.market_data import OpenSourceMarketDataProvider
from datetime import date

router = APIRouter()

@router.get("/market/live-quotes")
def get_live_market_quotes(
    symbols: Optional[str] = Query(None, description="Comma-separated tickers e.g. RELIANCE,HDFCBANK,TCS,NVDA"),
    db: Session = Depends(get_db)
):
    """
    Fetches real-time NSE & US stock exchange quotes via open source NSE / Yahoo Finance API (.NS tickers).
    100% Free, Zero API Key required.
    """
    if symbols:
        ticker_list = [s.strip().upper() for s in symbols.split(",") if s.strip()]
    else:
        stocks = db.query(StockMaster.ticker).all()
        ticker_list = [s[0] for s in stocks] if stocks else ["RELIANCE", "HDFCBANK", "TCS", "INFY", "NVDA"]

    provider = OpenSourceMarketDataProvider()
    live_quotes = provider.fetch_live_stock_quotes(ticker_list)
    
    return {
        "count": len(live_quotes),
        "data_source": "NSE Exchange Open API (Zero Key)",
        "quotes": live_quotes
    }

@router.post("/market/refresh-prices")
def refresh_database_live_prices(db: Session = Depends(get_db)):
    """
    Fetches fresh live exchange prices via open source APIs and updates database.
    """
    stocks = db.query(StockMaster).all()
    ticker_list = [s.ticker for s in stocks]
    
    provider = OpenSourceMarketDataProvider()
    live_quotes = provider.fetch_live_stock_quotes(ticker_list)
    
    updated_count = 0
    today = date.today()
    
    for stk in stocks:
        if stk.ticker in live_quotes:
            quote = live_quotes[stk.ticker]
            new_price = quote["last_price"]
            if new_price > 0:
                stk.current_price = new_price
                
                existing_ph = db.query(PriceHistory).filter(
                    PriceHistory.symbol == stk.ticker,
                    PriceHistory.price_date == today
                ).first()
                
                if not existing_ph:
                    db.add(PriceHistory(symbol=stk.ticker, price_date=today, close_price=new_price, volume=quote.get("volume", 0.0)))
                else:
                    existing_ph.close_price = new_price
                    
                updated_count += 1

    db.commit()
    return {
        "status": "SUCCESS",
        "data_source": "Open Source Market Data Engine",
        "updated_stocks_count": updated_count,
        "quotes_sample": live_quotes
    }
