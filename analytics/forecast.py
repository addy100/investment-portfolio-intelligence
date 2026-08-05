import numpy as np
from typing import Dict, Any, List

def run_monte_carlo_simulation(
    current_value: float,
    monthly_sip: float = 10000.0,
    expected_cagr: float = 12.0,
    volatility: float = 15.0,
    inflation_rate: float = 6.0,
    horizon_years: int = 10,
    target_goal: float = 5000000.0,
    num_simulations: int = 1000
) -> Dict[str, Any]:
    """
    Executes a Monte Carlo simulation of future portfolio wealth over a target horizon.
    Includes monthly SIP contributions and inflation adjustments.
    """
    months = horizon_years * 12
    monthly_mu = (1.0 + expected_cagr / 100.0) ** (1.0 / 12.0) - 1.0
    monthly_vol = (volatility / 100.0) / np.sqrt(12)
    
    # Log-normal parameters
    mu_log = np.log(1.0 + monthly_mu) - 0.5 * (monthly_vol ** 2)
    
    # Generate random return paths (num_simulations x months)
    simulated_returns = np.random.lognormal(mu_log, monthly_vol, (num_simulations, months)) - 1.0
    
    # Initialize trajectory matrix
    trajectories = np.zeros((num_simulations, months + 1))
    trajectories[:, 0] = current_value
    
    for m in range(1, months + 1):
        # Portfolio value grows by return + SIP contribution
        trajectories[:, m] = trajectories[:, m - 1] * (1.0 + simulated_returns[:, m - 1]) + monthly_sip

    final_values = trajectories[:, -1]
    
    # Calculate key percentiles
    worst_10th = float(np.percentile(final_values, 10))
    median_50th = float(np.percentile(final_values, 50))
    expected_mean = float(np.mean(final_values))
    best_90th = float(np.percentile(final_values, 90))
    
    success_count = np.sum(final_values >= target_goal)
    probability_success = float((success_count / num_simulations) * 100.0)

    # Real inflation-adjusted values
    real_factor = (1.0 + inflation_rate / 100.0) ** horizon_years
    
    # Build yearly fan-chart curve points for UI visualization
    yearly_steps = list(range(0, horizon_years + 1))
    yearly_10th = [float(np.percentile(trajectories[:, y * 12], 10)) for y in yearly_steps]
    yearly_50th = [float(np.percentile(trajectories[:, y * 12], 50)) for y in yearly_steps]
    yearly_90th = [float(np.percentile(trajectories[:, y * 12], 90)) for y in yearly_steps]

    return {
        "horizon_years": horizon_years,
        "current_value": current_value,
        "monthly_sip": monthly_sip,
        "target_goal": target_goal,
        "worst_case_10th": round(worst_10th, 2),
        "median_50th": round(median_50th, 2),
        "expected_mean": round(expected_mean, 2),
        "best_case_90th": round(best_90th, 2),
        "real_inflation_adjusted_median": round(median_50th / real_factor, 2),
        "success_probability": round(probability_success, 1),
        "yearly_trajectory": {
            "years": yearly_steps,
            "worst_10th": [round(v, 2) for v in yearly_10th],
            "median_50th": [round(v, 2) for v in yearly_50th],
            "best_90th": [round(v, 2) for v in yearly_90th],
        }
    }
