import csv
from datetime import datetime
from typing import List, Dict, Any

def parse_zerodha_holdings_csv(csv_content: str) -> List[Dict[str, Any]]:
    """
    Parses Zerodha holdings CSV export into standardized portfolio transaction dictionaries.
    Expected columns: Instrument, ISIN, Quantity, Average Price, Last Price, Cur. val
    """
    reader = csv.DictReader(csv_content.splitlines())
    holdings = []
    
    for row in reader:
        symbol = row.get("Instrument", "").strip()
        qty = float(row.get("Quantity", row.get("Qty.", 0)))
        avg_price = float(row.get("Average Price", row.get("Avg. cost", 0)))
        isin = row.get("ISIN", "").strip()
        
        if symbol and qty > 0:
            holdings.append({
                "asset_type": "STOCK",
                "symbol": symbol,
                "isin": isin,
                "units": qty,
                "avg_price": avg_price,
                "invested_amount": qty * avg_price
            })
            
    return holdings

def parse_zerodha_tradebook_csv(csv_content: str) -> List[Dict[str, Any]]:
    """
    Parses Zerodha Tradebook CSV export containing transaction history.
    Expected columns: symbol, trade_date, trade_type, quantity, price
    """
    reader = csv.DictReader(csv_content.splitlines())
    transactions = []
    
    for row in reader:
        symbol = row.get("symbol", "").strip()
        t_type = row.get("trade_type", "").strip().upper() # buy / sell
        qty = float(row.get("quantity", 0))
        price = float(row.get("price", 0))
        t_date_str = row.get("trade_date", "").strip()
        
        try:
            t_date = datetime.strptime(t_date_str, "%Y-%m-%d").date()
        except ValueError:
            t_date = datetime.now().date()
            
        if symbol and qty > 0:
            transactions.append({
                "asset_type": "STOCK",
                "symbol": symbol,
                "transaction_type": t_type,
                "transaction_date": t_date,
                "units": qty,
                "price": price,
                "total_amount": qty * price
            })
            
    return transactions
