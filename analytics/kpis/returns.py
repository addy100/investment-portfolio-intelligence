import numpy as np
from datetime import date
from typing import List, Tuple

def calculate_cagr(start_value: float, end_value: float, num_years: float) -> float:
    """Calculates Compound Annual Growth Rate (CAGR)."""
    if start_value <= 0 or num_years <= 0:
        return 0.0
    return ((end_value / start_value) ** (1.0 / num_years) - 1.0) * 100.0

def calculate_xirr(cash_flows: List[Tuple[date, float]], guess: float = 0.1) -> float:
    """
    Calculates Extended Internal Rate of Return (XIRR) using Newton-Raphson method.
    cash_flows: List of (date, amount) tuples where investments are negative and current value is positive.
    """
    if not cash_flows or len(cash_flows) < 2:
        return 0.0
        
    start_date = min(c[0] for c in cash_flows)
    
    def xnpv(rate):
        if rate <= -1.0:
            return 1e9
        return sum(
            cf / (1.0 + rate) ** ((dt - start_date).days / 365.0)
            for dt, cf in cash_flows
        )
        
    def xnpv_prime(rate):
        if rate <= -1.0:
            return 1e9
        return sum(
            -((dt - start_date).days / 365.0) * cf / (1.0 + rate) ** (((dt - start_date).days / 365.0) + 1.0)
            for dt, cf in cash_flows
        )

    r = guess
    for _ in range(100):
        f = xnpv(r)
        if abs(f) < 1e-5:
            return r * 100.0
        df = xnpv_prime(r)
        if abs(df) < 1e-7:
            break
        r = r - f / df
        
    return r * 100.0

def calculate_alpha_beta(returns: np.ndarray, benchmark_returns: np.ndarray, risk_free_rate: float = 0.06) -> Tuple[float, float, float]:
    """
    Calculates Beta, Alpha, and Jensen's Alpha relative to benchmark.
    Returns: (beta, alpha, jensen_alpha)
    """
    if len(returns) < 5 or len(benchmark_returns) < 5:
        return 1.0, 0.0, 0.0
        
    rf_daily = (1.0 + risk_free_rate) ** (1.0 / 252.0) - 1.0
    
    cov_matrix = np.cov(returns, benchmark_returns)
    if cov_matrix[1, 1] == 0:
        beta = 1.0
    else:
        beta = float(cov_matrix[0, 1] / cov_matrix[1, 1])
        
    mean_ret = np.mean(returns) * 252.0
    mean_bench = np.mean(benchmark_returns) * 252.0
    
    alpha = float((mean_ret - mean_bench) * 100.0)
    jensen_alpha = float((mean_ret - (risk_free_rate + beta * (mean_bench - risk_free_rate))) * 100.0)
    
    return beta, alpha, jensen_alpha

def calculate_information_ratio(returns: np.ndarray, benchmark_returns: np.ndarray) -> float:
    """Calculates Information Ratio = (Mean Active Return) / (Tracking Error)."""
    diff = returns - benchmark_returns
    tracking_error = np.std(diff) * np.sqrt(252)
    if tracking_error == 0:
        return 0.0
    active_return = np.mean(diff) * 252.0
    return float((active_return / tracking_error))
