# Power BI Integration Guide

Connect Power BI Desktop to the Portfolio Intelligence FastAPI backend for dynamic reporting.

## 1. Connect Power BI to FastAPI REST Endpoints

1. Open Power BI Desktop.
2. Click **Get Data** -> **Web**.
3. Select **Basic** and enter endpoint URL:
   - Portfolio Summary: `http://localhost:8000/api/portfolio`
   - Look-through Stock Holdings: `http://localhost:8000/api/holdings`
   - Risk Metrics: `http://localhost:8000/api/risk`
   - Monte Carlo Forecast: `http://localhost:8000/api/forecast`

## 2. Power Query (M-Code) Example for Holdings Endpoint

```powerquery
let
    Source = Json.Document(Web.Contents("http://localhost:8000/api/holdings")),
    lookthrough_stocks = Source[lookthrough_stocks],
    #"Converted to Table" = Table.FromList(lookthrough_stocks, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Expanded Column" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", {"ticker", "company_name", "sector", "country", "direct_value", "indirect_value", "total_value", "effective_weight"})
in
    #"Expanded Column"
```

## 3. Pre-Configured DAX Measures

- **Total Portfolio Value**: `SUM(LookthroughHoldings[total_value])`
- **Total Invested**: `SUM(Transactions[total_amount])`
- **Unrealized Gain**: `[Total Portfolio Value] - [Total Invested]`
- **Sharpe Ratio**: `AVERAGE(RiskMetrics[sharpe_ratio])`
