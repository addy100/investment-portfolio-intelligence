from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import FundMaster, FundHoldings

def calculate_pairwise_overlap(holdings_a: Dict[str, float], holdings_b: Dict[str, float]) -> Dict[str, Any]:
    """
    Calculates overlap percentage between two funds based on shared stock weights.
    Formula: Overlap % = Sum( min(weight_a_i, weight_b_i) )
    """
    common_stocks = set(holdings_a.keys()).intersection(set(holdings_b.keys()))
    shared_details = []
    total_overlap_pct = 0.0
    
    for ticker in common_stocks:
        w_a = holdings_a[ticker]
        w_b = holdings_b[ticker]
        min_weight = min(w_a, w_b)
        total_overlap_pct += min_weight
        shared_details.append({
            "ticker": ticker,
            "weight_fund_a": w_a,
            "weight_fund_b": w_b,
            "overlap_weight": round(min_weight, 2)
        })
        
    shared_details.sort(key=lambda x: x["overlap_weight"], reverse=True)
    return {
        "overlap_percentage": round(total_overlap_pct, 2),
        "common_stocks_count": len(common_stocks),
        "shared_holdings": shared_details
    }

def compute_portfolio_overlap_matrix(db: Session, scheme_codes: List[str]) -> Dict[str, Any]:
    """
    Generates a full N x N pairwise overlap matrix for all mutual funds in the portfolio.
    Also computes HHI index and Effective Number of Stocks.
    """
    fund_names: Dict[str, str] = {}
    fund_holdings_map: Dict[str, Dict[str, float]] = {}
    
    for code in scheme_codes:
        f_info = db.query(FundMaster).filter(FundMaster.scheme_code == code).first()
        fund_names[code] = f_info.fund_name if f_info else code
        
        holdings = db.query(FundHoldings).filter(FundHoldings.scheme_code == code).all()
        fund_holdings_map[code] = {h.stock_ticker: h.holding_percentage for h in holdings}

    matrix = []
    pairwise_results = []
    
    for i, code1 in enumerate(scheme_codes):
        row = []
        for j, code2 in enumerate(scheme_codes):
            if code1 == code2:
                overlap_val = 100.0
            else:
                res = calculate_pairwise_overlap(fund_holdings_map[code1], fund_holdings_map[code2])
                overlap_val = res["overlap_percentage"]
                if i < j:
                    pairwise_results.append({
                        "fund_a": fund_names[code1],
                        "fund_b": fund_names[code2],
                        "overlap_percentage": overlap_val,
                        "common_stocks": res["common_stocks_count"],
                        "shared_holdings": res["shared_holdings"]
                    })
            row.append(overlap_val)
        matrix.append({
            "scheme_code": code1,
            "fund_name": fund_names[code1],
            "overlaps": row
        })

    return {
        "funds": [{"scheme_code": c, "fund_name": fund_names[c]} for c in scheme_codes],
        "matrix": matrix,
        "pairwise_details": pairwise_results
    }

def calculate_hhi_and_effective_stocks(stock_weights: List[float]) -> Dict[str, float]:
    """
    Calculates Herfindahl-Hirschman Index (HHI) and Effective Number of Stocks (1 / HHI).
    stock_weights: List of weights in percentage (e.g. [15.2, 10.5, 5.0])
    """
    if not stock_weights or sum(stock_weights) == 0:
        return {"hhi": 0.0, "effective_num_stocks": 0.0}
        
    # Convert percentages to proportions (0 to 1)
    props = [w / 100.0 for w in stock_weights if w > 0]
    hhi = sum(p ** 2 for p in props)
    eff_stocks = 1.0 / hhi if hhi > 0 else 0.0
    
    return {
        "hhi": round(hhi * 10000.0, 2), # Standard 0 to 10,000 scale
        "effective_num_stocks": round(eff_stocks, 1)
    }
