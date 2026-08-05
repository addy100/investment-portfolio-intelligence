from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class SectorMaster(Base):
    __tablename__ = "Sector_Master"
    
    sector_id = Column(Integer, primary_key=True, index=True)
    sector_name = Column(String(100), unique=True, nullable=False)
    macro_sector = Column(String(100))
    benchmark_weight = Column(Float, default=0.0)

class StockMaster(Base):
    __tablename__ = "Stock_Master"
    
    stock_id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(50), unique=True, nullable=False)
    isin = Column(String(50))
    company_name = Column(String(200), nullable=False)
    sector_name = Column(String(100))
    market_cap_cat = Column(String(50), default="LARGE")
    country = Column(String(50), default="India")
    current_price = Column(Float, default=0.0)

class FundMaster(Base):
    __tablename__ = "Fund_Master"
    
    fund_id = Column(Integer, primary_key=True, index=True)
    scheme_code = Column(String(50), unique=True, nullable=False)
    isin = Column(String(50))
    fund_name = Column(String(200), nullable=False)
    amc = Column(String(100), nullable=False)
    category = Column(String(100))
    sub_category = Column(String(100))
    expense_ratio = Column(Float, default=0.0)
    turnover_ratio = Column(Float, default=0.0)
    benchmark_index = Column(String(100))

class FundNAV(Base):
    __tablename__ = "Fund_NAV"
    
    nav_id = Column(Integer, primary_key=True, index=True)
    scheme_code = Column(String(50), nullable=False, index=True)
    nav_date = Column(Date, nullable=False)
    nav = Column(Float, nullable=False)

class FundHoldings(Base):
    __tablename__ = "Fund_Holdings"
    
    holding_id = Column(Integer, primary_key=True, index=True)
    scheme_code = Column(String(50), nullable=False, index=True)
    as_of_date = Column(Date, nullable=False)
    stock_ticker = Column(String(50), nullable=False)
    holding_percentage = Column(Float, nullable=False)
    shares_held = Column(Float, default=0.0)
    market_value = Column(Float, default=0.0)

class ETFHoldings(Base):
    __tablename__ = "ETF_Holdings"
    
    etf_holding_id = Column(Integer, primary_key=True, index=True)
    etf_ticker = Column(String(50), nullable=False, index=True)
    as_of_date = Column(Date, nullable=False)
    stock_ticker = Column(String(50), nullable=False)
    holding_percentage = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)

class Portfolio(Base):
    __tablename__ = "Portfolio"
    
    portfolio_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    owner = Column(String(100), default="User")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transactions = relationship("Transaction", back_populates="portfolio")

class Transaction(Base):
    __tablename__ = "Transactions"
    
    transaction_id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("Portfolio.portfolio_id"), nullable=False)
    asset_type = Column(String(20), nullable=False) # STOCK, MF, ETF
    asset_symbol = Column(String(50), nullable=False)
    transaction_date = Column(Date, nullable=False)
    transaction_type = Column(String(10), nullable=False) # BUY, SELL, SIP
    units = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    fees = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    
    portfolio = relationship("Portfolio", back_populates="transactions")

class PriceHistory(Base):
    __tablename__ = "Price_History"
    
    price_id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(50), nullable=False, index=True)
    price_date = Column(Date, nullable=False)
    close_price = Column(Float, nullable=False)
    benchmark_price = Column(Float, default=0.0)
    volume = Column(Float, default=0.0)

class RiskMetrics(Base):
    __tablename__ = "RiskMetrics"
    
    metric_id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, nullable=False)
    asset_symbol = Column(String(50))
    calculation_date = Column(Date, nullable=False)
    sharpe_ratio = Column(Float)
    sortino_ratio = Column(Float)
    treynor_ratio = Column(Float)
    var_95 = Column(Float)
    cvar_95 = Column(Float)
    max_drawdown = Column(Float)
    volatility = Column(Float)
    beta = Column(Float)
    alpha = Column(Float)
    tracking_error = Column(Float)

class Forecast(Base):
    __tablename__ = "Forecast"
    
    forecast_id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, nullable=False)
    calculation_date = Column(Date, nullable=False)
    horizon_years = Column(Integer, nullable=False)
    worst_case_10th = Column(Float)
    median_50th = Column(Float)
    expected_mean = Column(Float)
    best_case_90th = Column(Float)
    success_probability = Column(Float)

class AIQueryLog(Base):
    __tablename__ = "AI_Query_Log"
    
    log_id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    sql_generated = Column(Text)
    answer_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
