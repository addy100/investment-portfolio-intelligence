# Portfolio Intelligence API Specification

## Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/portfolio` | Top-level portfolio valuation, XIRR returns, and sector concentration. |
| `GET` | `/api/funds` | Fund Master list, scheme codes, and expense ratios. |
| `GET` | `/api/holdings` | Direct stocks + deep look-through indirect stock exposures. |
| `GET` | `/api/overlap` | Pairwise mutual fund overlap matrix and shared holdings details. |
| `GET` | `/api/forecast` | Monte Carlo forecast simulation over 5/10/15 year horizons. |
| `GET` | `/api/risk` | Sharpe ratio, Sortino, VaR 95%, Max Drawdown, capture ratios. |
| `GET` | `/api/recommendation` | Portfolio optimization & expense reduction recommendations. |
| `GET` | `/api/excel` | Dynamic Excel binary file download (`.xlsx`). |
| `GET` | `/api/powerbi` | Power BI dataset schema and DAX definitions. |
| `POST` | `/api/ai/query` | Natural language portfolio assistant query endpoint. |
