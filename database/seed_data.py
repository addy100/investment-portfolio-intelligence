import sys
import os
from datetime import date, timedelta
import random

# Add parent directory to path so we can import backend models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.db.database import Base, engine, SessionLocal
from app.models.models import (
    SectorMaster, StockMaster, FundMaster, FundNAV, FundHoldings,
    ETFHoldings, Portfolio, Transaction, PriceHistory, RiskMetrics,
    Forecast, AIQueryLog
)

def seed_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(Portfolio).first():
        print("Database already contains data. Skipping seed.")
        db.close()
        return

    print("Seeding Sector Master...")
    sectors = [
        SectorMaster(sector_name="Financials", macro_sector="Services", benchmark_weight=33.5),
        SectorMaster(sector_name="Information Technology", macro_sector="Technology", benchmark_weight=13.8),
        SectorMaster(sector_name="Oil Gas & Consumable Fuels", macro_sector="Energy", benchmark_weight=11.2),
        SectorMaster(sector_name="Consumer Goods", macro_sector="Consumer", benchmark_weight=9.4),
        SectorMaster(sector_name="Automobile & Auto Components", macro_sector="Manufacturing", benchmark_weight=6.5),
        SectorMaster(sector_name="US Technology", macro_sector="Global Tech", benchmark_weight=15.0),
        SectorMaster(sector_name="Healthcare & Pharma", macro_sector="Healthcare", benchmark_weight=5.6),
    ]
    db.add_all(sectors)
    db.commit()

    print("Seeding Stock Master...")
    stocks = [
        StockMaster(ticker="RELIANCE", isin="INE002A01018", company_name="Reliance Industries Ltd.", sector_name="Oil Gas & Consumable Fuels", market_cap_cat="LARGE", country="India", current_price=2950.0),
        StockMaster(ticker="HDFCBANK", isin="INE040A01034", company_name="HDFC Bank Ltd.", sector_name="Financials", market_cap_cat="LARGE", country="India", current_price=1620.0),
        StockMaster(ticker="TCS", isin="INE467B01029", company_name="Tata Consultancy Services Ltd.", sector_name="Information Technology", market_cap_cat="LARGE", country="India", current_price=4180.0),
        StockMaster(ticker="INFY", isin="INE009A01021", company_name="Infosys Ltd.", sector_name="Information Technology", market_cap_cat="LARGE", country="India", current_price=1810.0),
        StockMaster(ticker="ICICIBANK", isin="INE090A01021", company_name="ICICI Bank Ltd.", sector_name="Financials", market_cap_cat="LARGE", country="India", current_price=1180.0),
        StockMaster(ticker="ITC", isin="INE154A01025", company_name="ITC Ltd.", sector_name="Consumer Goods", market_cap_cat="LARGE", country="India", current_price=490.0),
        StockMaster(ticker="BHARTIARTL", isin="INE397D01024", company_name="Bharti Airtel Ltd.", sector_name="Services", market_cap_cat="LARGE", country="India", current_price=1450.0),
        StockMaster(ticker="NVDA", isin="US67066G1040", company_name="NVIDIA Corporation", sector_name="US Technology", market_cap_cat="LARGE", country="USA", current_price=125.0),
        StockMaster(ticker="AAPL", isin="US0378331005", company_name="Apple Inc.", sector_name="US Technology", market_cap_cat="LARGE", country="USA", current_price=220.0),
        StockMaster(ticker="MSFT", isin="US5949181045", company_name="Microsoft Corporation", sector_name="US Technology", market_cap_cat="LARGE", country="USA", current_price=440.0),
        StockMaster(ticker="GOOGL", isin="US02079K3059", company_name="Alphabet Inc.", sector_name="US Technology", market_cap_cat="LARGE", country="USA", current_price=175.0),
    ]
    db.add_all(stocks)
    db.commit()

    print("Seeding Fund Master...")
    funds = [
        FundMaster(scheme_code="120503", isin="INF846K01131", fund_name="Axis Bluechip Fund Direct Growth", amc="Axis Mutual Fund", category="Equity", sub_category="Large Cap", expense_ratio=0.62, turnover_ratio=28.0, benchmark_index="NIFTY 50 TRI"),
        FundMaster(scheme_code="122639", isin="INF879O01015", fund_name="Parag Parikh Flexi Cap Fund Direct Growth", amc="PPFAS Mutual Fund", category="Equity", sub_category="Flexi Cap", expense_ratio=0.58, turnover_ratio=18.5, benchmark_index="NIFTY 500 TRI"),
        FundMaster(scheme_code="125497", isin="INF200K01VG9", fund_name="SBI Small Cap Fund Direct Growth", amc="SBI Mutual Fund", category="Equity", sub_category="Small Cap", expense_ratio=0.69, turnover_ratio=35.0, benchmark_index="NIFTY Smallcap 250 TRI"),
        FundMaster(scheme_code="NIFTYBEES", isin="INF732E01037", fund_name="Nippon India ETF Nifty BeES", amc="Nippon India Mutual Fund", category="ETF", sub_category="Index ETF", expense_ratio=0.04, turnover_ratio=5.0, benchmark_index="NIFTY 50 TRI"),
    ]
    db.add_all(funds)
    db.commit()

    print("Seeding Fund Holdings...")
    fund_holdings = [
        # Axis Bluechip Fund
        FundHoldings(scheme_code="120503", as_of_date=date.today(), stock_ticker="ICICIBANK", holding_percentage=9.5, shares_held=450000.0, market_value=531000000.0),
        FundHoldings(scheme_code="120503", as_of_date=date.today(), stock_ticker="HDFCBANK", holding_percentage=9.1, shares_held=320000.0, market_value=518400000.0),
        FundHoldings(scheme_code="120503", as_of_date=date.today(), stock_ticker="RELIANCE", holding_percentage=8.2, shares_held=160000.0, market_value=472000000.0),
        FundHoldings(scheme_code="120503", as_of_date=date.today(), stock_ticker="TCS", holding_percentage=7.0, shares_held=95000.0, market_value=397100000.0),
        FundHoldings(scheme_code="120503", as_of_date=date.today(), stock_ticker="INFY", holding_percentage=6.4, shares_held=210000.0, market_value=380100000.0),
        
        # Parag Parikh Flexi Cap
        FundHoldings(scheme_code="122639", as_of_date=date.today(), stock_ticker="HDFCBANK", holding_percentage=8.1, shares_held=800000.0, market_value=1296000000.0),
        FundHoldings(scheme_code="122639", as_of_date=date.today(), stock_ticker="GOOGL", holding_percentage=6.2, shares_held=560000.0, market_value=980000000.0),
        FundHoldings(scheme_code="122639", as_of_date=date.today(), stock_ticker="MSFT", holding_percentage=5.8, shares_held=210000.0, market_value=924000000.0),
        FundHoldings(scheme_code="122639", as_of_date=date.today(), stock_ticker="NVDA", holding_percentage=4.5, shares_held=580000.0, market_value=725000000.0),
        FundHoldings(scheme_code="122639", as_of_date=date.today(), stock_ticker="ITC", holding_percentage=5.2, shares_held=1700000.0, market_value=833000000.0),

        # SBI Small Cap Fund
        FundHoldings(scheme_code="125497", as_of_date=date.today(), stock_ticker="BHARTIARTL", holding_percentage=4.2, shares_held=300000.0, market_value=435000000.0),
        FundHoldings(scheme_code="125497", as_of_date=date.today(), stock_ticker="ITC", holding_percentage=3.8, shares_held=800000.0, market_value=392000000.0),
    ]
    db.add_all(fund_holdings)

    # ETF Holdings for NIFTYBEES
    etf_holdings = [
        ETFHoldings(etf_ticker="NIFTYBEES", as_of_date=date.today(), stock_ticker="HDFCBANK", holding_percentage=11.5, weight=0.115),
        ETFHoldings(etf_ticker="NIFTYBEES", as_of_date=date.today(), stock_ticker="RELIANCE", holding_percentage=10.2, weight=0.102),
        ETFHoldings(etf_ticker="NIFTYBEES", as_of_date=date.today(), stock_ticker="ICICIBANK", holding_percentage=7.8, weight=0.078),
        ETFHoldings(etf_ticker="NIFTYBEES", as_of_date=date.today(), stock_ticker="INFY", holding_percentage=5.9, weight=0.059),
        ETFHoldings(etf_ticker="NIFTYBEES", as_of_date=date.today(), stock_ticker="TCS", holding_percentage=4.1, weight=0.041),
    ]
    db.add_all(etf_holdings)
    db.commit()

    print("Seeding Portfolio & Transactions...")
    p = Portfolio(name="Wealth Builder Alpha", description="Main Long Term Equity & Mutual Fund Portfolio", owner="John Doe")
    db.add(p)
    db.commit()

    start_date = date.today() - timedelta(days=365)
    txs = [
        # Direct Stocks
        Transaction(portfolio_id=p.portfolio_id, asset_type="STOCK", asset_symbol="RELIANCE", transaction_date=start_date, transaction_type="BUY", units=50, price=2450.0, total_amount=122500.0),
        Transaction(portfolio_id=p.portfolio_id, asset_type="STOCK", asset_symbol="HDFCBANK", transaction_date=start_date + timedelta(days=30), transaction_type="BUY", units=100, price=1480.0, total_amount=148000.0),
        Transaction(portfolio_id=p.portfolio_id, asset_type="STOCK", asset_symbol="NVDA", transaction_date=start_date + timedelta(days=60), transaction_type="BUY", units=80, price=85.0, total_amount=6800.0),
        
        # Mutual Funds
        Transaction(portfolio_id=p.portfolio_id, asset_type="MF", asset_symbol="120503", transaction_date=start_date, transaction_type="SIP", units=2500, price=45.2, total_amount=113000.0),
        Transaction(portfolio_id=p.portfolio_id, asset_type="MF", asset_symbol="122639", transaction_date=start_date, transaction_type="SIP", units=3000, price=52.8, total_amount=158400.0),
        Transaction(portfolio_id=p.portfolio_id, asset_type="MF", asset_symbol="125497", transaction_date=start_date + timedelta(days=90), transaction_type="SIP", units=1500, price=112.5, total_amount=168750.0),

        # ETF
        Transaction(portfolio_id=p.portfolio_id, asset_type="ETF", asset_symbol="NIFTYBEES", transaction_date=start_date + timedelta(days=120), transaction_type="BUY", units=500, price=240.0, total_amount=120000.0),
    ]
    db.add_all(txs)
    db.commit()

    print("Seeding Price History & NAV History...")
    current_date = start_date
    nav_120503 = 45.2
    nav_122639 = 52.8
    nav_125497 = 112.5
    price_reliance = 2450.0
    price_hdfc = 1480.0
    price_nvda = 85.0
    
    while current_date <= date.today():
        # NAV entries
        db.add(FundNAV(scheme_code="120503", nav_date=current_date, nav=round(nav_120503, 4)))
        db.add(FundNAV(scheme_code="122639", nav_date=current_date, nav=round(nav_122639, 4)))
        db.add(FundNAV(scheme_code="125497", nav_date=current_date, nav=round(nav_125497, 4)))
        
        # Stock prices
        db.add(PriceHistory(symbol="RELIANCE", price_date=current_date, close_price=round(price_reliance, 2), benchmark_price=22000.0))
        db.add(PriceHistory(symbol="HDFCBANK", price_date=current_date, close_price=round(price_hdfc, 2), benchmark_price=22000.0))
        db.add(PriceHistory(symbol="NVDA", price_date=current_date, close_price=round(price_nvda, 2), benchmark_price=5200.0))
        
        # Increment simulated prices with random walk
        nav_120503 *= (1 + random.uniform(-0.008, 0.009))
        nav_122639 *= (1 + random.uniform(-0.007, 0.0095))
        nav_125497 *= (1 + random.uniform(-0.012, 0.013))
        price_reliance *= (1 + random.uniform(-0.01, 0.011))
        price_hdfc *= (1 + random.uniform(-0.009, 0.01))
        price_nvda *= (1 + random.uniform(-0.015, 0.018))
        
        current_date += timedelta(days=7) # Weekly resolution for speed
        
    db.commit()

    print("Seeding Risk Metrics & Forecast...")
    rm = RiskMetrics(
        portfolio_id=p.portfolio_id,
        calculation_date=date.today(),
        sharpe_ratio=1.85,
        sortino_ratio=2.42,
        treynor_ratio=0.145,
        var_95=-1.85,
        cvar_95=-2.65,
        max_drawdown=-11.4,
        volatility=12.6,
        beta=0.92,
        alpha=4.8,
        tracking_error=2.1
    )
    db.add(rm)

    fc = Forecast(
        portfolio_id=p.portfolio_id,
        calculation_date=date.today(),
        horizon_years=10,
        worst_case_10th=1850000.0,
        median_50th=3200000.0,
        expected_mean=3450000.0,
        best_case_90th=5400000.0,
        success_probability=92.5
    )
    db.add(fc)
    db.commit()

    db.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
