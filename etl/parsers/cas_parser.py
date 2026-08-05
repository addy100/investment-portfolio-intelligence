from datetime import datetime
from typing import List, Dict, Any

def parse_cas_statement_data(statement_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Parses Consolidated Account Statement (CAS) rows into standardized Mutual Fund transaction entries.
    """
    parsed_entries = []
    
    for row in statement_rows:
        scheme_code = str(row.get("scheme_code", "")).strip()
        fund_name = row.get("fund_name", "").strip()
        txn_date_str = row.get("date", "").strip()
        txn_type = row.get("type", "PURCHASE").upper()
        units = float(row.get("units", 0.0))
        nav = float(row.get("nav", 0.0))
        amount = float(row.get("amount", units * nav))
        
        try:
            txn_date = datetime.strptime(txn_date_str, "%Y-%m-%d").date()
        except ValueError:
            txn_date = datetime.now().date()
            
        if scheme_code and units > 0:
            parsed_entries.append({
                "asset_type": "MF",
                "scheme_code": scheme_code,
                "fund_name": fund_name,
                "transaction_type": "SIP" if "SIP" in txn_type else "BUY",
                "transaction_date": txn_date,
                "units": units,
                "price": nav,
                "total_amount": amount
            })
            
    return parsed_entries
