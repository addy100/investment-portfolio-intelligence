from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import Transaction, StockMaster, FundMaster, FundHoldings, ETFHoldings, FundNAV, PriceHistory

def compute_lookthrough_holdings(db: Session, portfolio_id: int) -> Dict[str, Any]:
    """
    Computes total portfolio valuation and deep look-through stock exposure.
    Combines Direct Stock holdings + Mutual Fund underlying stocks + ETF underlying stocks.
    """
    transactions = db.query(Transaction).filter(Transaction.portfolio_id == portfolio_id).all()
    
    # Aggregate net units held per asset
    asset_units: Dict[str, Dict[str, Any]] = {}
    for tx in transactions:
        key = (tx.asset_type, tx.asset_symbol)
        if key not in asset_units:
            asset_units[key] = {"asset_type": tx.asset_type, "symbol": tx.asset_symbol, "units": 0.0, "invested": 0.0}
        
        if tx.transaction_type in ["BUY", "SIP"]:
            asset_units[key]["units"] += tx.units
            asset_units[key]["invested"] += tx.total_amount
        elif tx.transaction_type == "SELL":
            asset_units[key]["units"] -= tx.units
            asset_units[key]["invested"] -= tx.total_amount

    total_portfolio_value = 0.0
    direct_assets = []
    
    # Store effective underlying stock values
    stock_exposure: Dict[str, Dict[str, Any]] = {} # ticker -> {direct_value, indirect_value, total_value, sources}

    # Fetch latest prices/NAVs
    for key, data in asset_units.items():
        asset_type, symbol = key
        units = data["units"]
        if units <= 0:
            continue
            
        current_value = 0.0
        name = symbol
        
        if asset_type == "STOCK":
            stock_info = db.query(StockMaster).filter(StockMaster.ticker == symbol).first()
            price = stock_info.current_price if stock_info else 100.0
            name = stock_info.company_name if stock_info else symbol
            current_value = units * price
            
            # Record direct stock exposure
            if symbol not in stock_exposure:
                stock_exposure[symbol] = {
                    "ticker": symbol,
                    "company_name": name,
                    "sector": stock_info.sector_name if stock_info else "Unknown",
                    "country": stock_info.country if stock_info else "India",
                    "direct_value": 0.0,
                    "indirect_value": 0.0,
                    "total_value": 0.0,
                    "sources": []
                }
            stock_exposure[symbol]["direct_value"] += current_value
            stock_exposure[symbol]["total_value"] += current_value
            stock_exposure[symbol]["sources"].append({
                "source": "Direct Equity",
                "percentage": 100.0,
                "value": current_value
            })
            
        elif asset_type == "MF":
            fund_info = db.query(FundMaster).filter(FundMaster.scheme_code == symbol).first()
            latest_nav_entry = db.query(FundNAV).filter(FundNAV.scheme_code == symbol).order_by(FundNAV.nav_date.desc()).first()
            nav = latest_nav_entry.nav if latest_nav_entry else 50.0
            name = fund_info.fund_name if fund_info else symbol
            current_value = units * nav
            
            # Unravel MF holdings
            holdings = db.query(FundHoldings).filter(FundHoldings.scheme_code == symbol).all()
            for h in holdings:
                underlying_val = current_value * (h.holding_percentage / 100.0)
                stk_ticker = h.stock_ticker
                
                stock_info = db.query(StockMaster).filter(StockMaster.ticker == stk_ticker).first()
                if stk_ticker not in stock_exposure:
                    stock_exposure[stk_ticker] = {
                        "ticker": stk_ticker,
                        "company_name": stock_info.company_name if stock_info else stk_ticker,
                        "sector": stock_info.sector_name if stock_info else "Unknown",
                        "country": stock_info.country if stock_info else "India",
                        "direct_value": 0.0,
                        "indirect_value": 0.0,
                        "total_value": 0.0,
                        "sources": []
                    }
                stock_exposure[stk_ticker]["indirect_value"] += underlying_val
                stock_exposure[stk_ticker]["total_value"] += underlying_val
                stock_exposure[stk_ticker]["sources"].append({
                    "source": f"Fund: {name}",
                    "percentage": h.holding_percentage,
                    "value": underlying_val
                })
                
        elif asset_type == "ETF":
            fund_info = db.query(FundMaster).filter(FundMaster.scheme_code == symbol).first()
            price = 250.0 # Default ETF price if not in DB
            name = fund_info.fund_name if fund_info else symbol
            current_value = units * price
            
            # Unravel ETF holdings
            holdings = db.query(ETFHoldings).filter(ETFHoldings.etf_ticker == symbol).all()
            for h in holdings:
                underlying_val = current_value * (h.holding_percentage / 100.0)
                stk_ticker = h.stock_ticker
                stock_info = db.query(StockMaster).filter(StockMaster.ticker == stk_ticker).first()
                
                if stk_ticker not in stock_exposure:
                    stock_exposure[stk_ticker] = {
                        "ticker": stk_ticker,
                        "company_name": stock_info.company_name if stock_info else stk_ticker,
                        "sector": stock_info.sector_name if stock_info else "Unknown",
                        "country": stock_info.country if stock_info else "India",
                        "direct_value": 0.0,
                        "indirect_value": 0.0,
                        "total_value": 0.0,
                        "sources": []
                    }
                stock_exposure[stk_ticker]["indirect_value"] += underlying_val
                stock_exposure[stk_ticker]["total_value"] += underlying_val
                stock_exposure[stk_ticker]["sources"].append({
                    "source": f"ETF: {name}",
                    "percentage": h.holding_percentage,
                    "value": underlying_val
                })

        total_portfolio_value += current_value
        direct_assets.append({
            "asset_type": asset_type,
            "symbol": symbol,
            "name": name,
            "units": units,
            "invested": data["invested"],
            "current_value": current_value,
            "gain_loss": current_value - data["invested"],
            "gain_loss_pct": ((current_value - data["invested"]) / data["invested"] * 100.0) if data["invested"] > 0 else 0.0
        })

    # Calculate portfolio weights for underlying stocks
    lookthrough_list = list(stock_exposure.values())
    for item in lookthrough_list:
        item["effective_weight"] = round((item["total_value"] / total_portfolio_value * 100.0), 2) if total_portfolio_value > 0 else 0.0
        item["direct_value"] = round(item["direct_value"], 2)
        item["indirect_value"] = round(item["indirect_value"], 2)
        item["total_value"] = round(item["total_value"], 2)

    lookthrough_list.sort(key=lambda x: x["total_value"], reverse=True)

    # Sector Breakdown
    sector_breakdown: Dict[str, float] = {}
    for item in lookthrough_list:
        sec = item["sector"]
        sector_breakdown[sec] = sector_breakdown.get(sec, 0.0) + item["total_value"]
        
    sector_list = [
        {"sector": sec, "value": round(val, 2), "weight": round((val / total_portfolio_value * 100.0), 2) if total_portfolio_value > 0 else 0.0}
        for sec, val in sector_breakdown.items()
    ]
    sector_list.sort(key=lambda x: x["value"], reverse=True)

    return {
        "total_portfolio_value": round(total_portfolio_value, 2),
        "total_invested": round(sum(a["invested"] for a in direct_assets), 2),
        "direct_assets": direct_assets,
        "lookthrough_stocks": lookthrough_list,
        "sector_breakdown": sector_list
    }
