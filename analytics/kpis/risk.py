import numpy as np
from typing import Tuple, Dict

def calculate_volatility(returns: np.ndarray, annualize: bool = True) -> float:
    """Calculates annual volatility (standard deviation)."""
    if len(returns) == 0:
        return 0.0
    vol = float(np.std(returns))
    if annualize:
        vol *= np.sqrt(252)
    return float(vol * 100.0)

def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.06) -> float:
    """Calculates Sharpe Ratio = (Annualized Return - Risk Free Rate) / Annualized Volatility."""
    if len(returns) < 2:
        return 0.0
    rf_daily = (1.0 + risk_free_rate) ** (1.0 / 252.0) - 1.0
    excess_returns = returns - rf_daily
    std = np.std(excess_returns)
    if std == 0:
        return 0.0
    sharpe = (np.mean(excess_returns) / std) * np.sqrt(252)
    return float(sharpe)

def calculate_sortino_ratio(returns: np.ndarray, risk_free_rate: float = 0.06) -> float:
    """Calculates Sortino Ratio = (Annualized Return - Risk Free Rate) / Downside Deviation."""
    if len(returns) < 2:
        return 0.0
    rf_daily = (1.0 + risk_free_rate) ** (1.0 / 252.0) - 1.0
    excess_returns = returns - rf_daily
    downside_returns = excess_returns[excess_returns < 0]
    if len(downside_returns) == 0:
        return 0.0
    downside_std = np.sqrt(np.mean(downside_returns ** 2))
    if downside_std == 0:
        return 0.0
    sortino = (np.mean(excess_returns) / downside_std) * np.sqrt(252)
    return float(sortino)

def calculate_var_cvar(returns: np.ndarray, confidence_level: float = 0.95) -> Tuple[float, float]:
    """
    Calculates Historical Value at Risk (VaR) and Conditional VaR (Expected Shortfall).
    Returns negative percentages representing potential loss.
    """
    if len(returns) == 0:
        return 0.0, 0.0
    sorted_returns = np.sort(returns)
    index = int((1.0 - confidence_level) * len(sorted_returns))
    var = sorted_returns[index]
    cvar = np.mean(sorted_returns[:index+1]) if index > 0 else var
    return float(var * 100.0), float(cvar * 100.0)

def calculate_max_drawdown(prices: np.ndarray) -> Tuple[float, int, int]:
    """
    Calculates Maximum Drawdown percentage and peak/trough indices.
    Returns: (max_drawdown_percent, peak_index, trough_index)
    """
    if len(prices) < 2:
        return 0.0, 0, 0
    cummax = np.maximum.accumulate(prices)
    drawdowns = (prices - cummax) / cummax
    max_dd_idx = np.argmin(drawdowns)
    peak_idx = np.argmax(prices[:max_dd_idx+1]) if max_dd_idx > 0 else 0
    max_dd_pct = float(drawdowns[max_dd_idx] * 100.0)
    return max_dd_pct, int(peak_idx), int(max_dd_idx)

def calculate_capture_ratios(returns: np.ndarray, benchmark_returns: np.ndarray) -> Tuple[float, float]:
    """
    Calculates Upside and Downside Capture Ratios relative to benchmark.
    Returns: (upside_capture, downside_capture)
    """
    if len(returns) < 5 or len(benchmark_returns) < 5:
        return 100.0, 100.0
        
    up_mask = benchmark_returns > 0
    down_mask = benchmark_returns < 0
    
    up_capture = (np.mean(returns[up_mask]) / np.mean(benchmark_returns[up_mask])) * 100.0 if np.sum(up_mask) > 0 else 100.0
    down_capture = (np.mean(returns[down_mask]) / np.mean(benchmark_returns[down_mask])) * 100.0 if np.sum(down_mask) > 0 else 100.0
    
    return float(up_capture), float(down_capture)

def calculate_all_risk_metrics(returns: np.ndarray, prices: np.ndarray, benchmark_returns: np.ndarray = None) -> Dict[str, float]:
    """Returns a dictionary containing all risk KPIs."""
    vol = calculate_volatility(returns)
    sharpe = calculate_sharpe_ratio(returns)
    sortino = calculate_sortino_ratio(returns)
    var95, cvar95 = calculate_var_cvar(returns, 0.95)
    max_dd, _, _ = calculate_max_drawdown(prices)
    
    up_cap, down_cap = (100.0, 100.0)
    if benchmark_returns is not None and len(benchmark_returns) == len(returns):
        up_cap, down_cap = calculate_capture_ratios(returns, benchmark_returns)
        
    return {
        "volatility": vol,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "var_95": var95,
        "cvar_95": cvar95,
        "max_drawdown": max_dd,
        "upside_capture": up_cap,
        "downside_capture": down_cap
    }
