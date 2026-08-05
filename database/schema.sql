-- Portfolio Intelligence DDL Schema
-- Compatible with PostgreSQL & SQLite

CREATE TABLE IF NOT EXISTS Sector_Master (
    sector_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_name VARCHAR(100) NOT NULL UNIQUE,
    macro_sector VARCHAR(100),
    benchmark_weight DECIMAL(5,2) DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS Stock_Master (
    stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker VARCHAR(50) NOT NULL UNIQUE,
    isin VARCHAR(50),
    company_name VARCHAR(200) NOT NULL,
    sector_name VARCHAR(100),
    market_cap_cat VARCHAR(50) DEFAULT 'LARGE', -- LARGE, MID, SMALL
    country VARCHAR(50) DEFAULT 'India',
    current_price DECIMAL(12,2) DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS Fund_Master (
    fund_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code VARCHAR(50) NOT NULL UNIQUE,
    isin VARCHAR(50),
    fund_name VARCHAR(200) NOT NULL,
    amc VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    sub_category VARCHAR(100),
    expense_ratio DECIMAL(5,3) DEFAULT 0.0,
    turnover_ratio DECIMAL(5,2) DEFAULT 0.0,
    benchmark_index VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Fund_NAV (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code VARCHAR(50) NOT NULL,
    nav_date DATE NOT NULL,
    nav DECIMAL(12,4) NOT NULL,
    UNIQUE(scheme_code, nav_date)
);

CREATE TABLE IF NOT EXISTS Fund_Holdings (
    holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code VARCHAR(50) NOT NULL,
    as_of_date DATE NOT NULL,
    stock_ticker VARCHAR(50) NOT NULL,
    holding_percentage DECIMAL(6,3) NOT NULL,
    shares_held DECIMAL(15,2) DEFAULT 0.0,
    market_value DECIMAL(18,2) DEFAULT 0.0
);

CREATE TABLE IF NOT EXISTS ETF_Holdings (
    etf_holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    etf_ticker VARCHAR(50) NOT NULL,
    as_of_date DATE NOT NULL,
    stock_ticker VARCHAR(50) NOT NULL,
    holding_percentage DECIMAL(6,3) NOT NULL,
    weight DECIMAL(6,3) NOT NULL
);

CREATE TABLE IF NOT EXISTS Portfolio (
    portfolio_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    owner VARCHAR(100) DEFAULT 'User',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    asset_type VARCHAR(20) NOT NULL, -- STOCK, MF, ETF
    asset_symbol VARCHAR(50) NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(10) NOT NULL, -- BUY, SELL, SIP
    units DECIMAL(15,4) NOT NULL,
    price DECIMAL(12,4) NOT NULL,
    fees DECIMAL(10,2) DEFAULT 0.0,
    total_amount DECIMAL(18,2) NOT NULL,
    FOREIGN KEY (portfolio_id) REFERENCES Portfolio(portfolio_id)
);

CREATE TABLE IF NOT EXISTS Price_History (
    price_id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol VARCHAR(50) NOT NULL,
    price_date DATE NOT NULL,
    close_price DECIMAL(12,4) NOT NULL,
    benchmark_price DECIMAL(12,4) DEFAULT 0.0,
    volume DECIMAL(18,2) DEFAULT 0.0,
    UNIQUE(symbol, price_date)
);

CREATE TABLE IF NOT EXISTS RiskMetrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    asset_symbol VARCHAR(50),
    calculation_date DATE NOT NULL,
    sharpe_ratio DECIMAL(8,4),
    sortino_ratio DECIMAL(8,4),
    treynor_ratio DECIMAL(8,4),
    var_95 DECIMAL(8,4),
    cvar_95 DECIMAL(8,4),
    max_drawdown DECIMAL(8,4),
    volatility DECIMAL(8,4),
    beta DECIMAL(8,4),
    alpha DECIMAL(8,4),
    tracking_error DECIMAL(8,4)
);

CREATE TABLE IF NOT EXISTS Forecast (
    forecast_id INTEGER PRIMARY KEY AUTOINCREMENT,
    portfolio_id INTEGER NOT NULL,
    calculation_date DATE NOT NULL,
    horizon_years INTEGER NOT NULL,
    worst_case_10th DECIMAL(18,2),
    median_50th DECIMAL(18,2),
    expected_mean DECIMAL(18,2),
    best_case_90th DECIMAL(18,2),
    success_probability DECIMAL(5,2)
);

CREATE TABLE IF NOT EXISTS AI_Query_Log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    sql_generated TEXT,
    answer_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
