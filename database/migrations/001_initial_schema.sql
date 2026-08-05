-- PostgreSQL / Supabase initial schema. Timestamps are stored in UTC.
create extension if not exists pgcrypto;

create table if not exists fund_master (
  fund_id uuid primary key default gen_random_uuid(),
  fund_code text not null unique,
  name text not null,
  amc_name text,
  category text,
  expense_ratio numeric(8,6),
  isin text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists stock_master (
  stock_id uuid primary key default gen_random_uuid(),
  isin text unique,
  ticker text,
  name text not null,
  sector text,
  country_code char(2),
  created_at timestamptz not null default now()
);

create table if not exists sector_master (
  sector_code text primary key,
  sector_name text not null,
  parent_sector_code text references sector_master(sector_code)
);

create table if not exists fund_nav (
  fund_id uuid not null references fund_master(fund_id),
  nav_date date not null,
  nav numeric(18,6) not null check (nav >= 0),
  source_url text,
  primary key (fund_id, nav_date)
);

create table if not exists fund_holdings (
  fund_id uuid not null references fund_master(fund_id),
  stock_id uuid references stock_master(stock_id),
  holding_name text not null,
  holding_date date not null,
  weight numeric(9,6) check (weight >= 0 and weight <= 1),
  primary key (fund_id, holding_name, holding_date)
);

create table if not exists etf_holdings (
  etf_id uuid not null references fund_master(fund_id),
  stock_id uuid references stock_master(stock_id),
  holding_name text not null,
  holding_date date not null,
  weight numeric(9,6) check (weight >= 0 and weight <= 1),
  primary key (etf_id, holding_name, holding_date)
);

create table if not exists portfolio (
  portfolio_id uuid primary key default gen_random_uuid(),
  portfolio_name text not null unique,
  base_currency char(3) not null default 'INR',
  created_at timestamptz not null default now()
);

create table if not exists transactions (
  transaction_id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references portfolio(portfolio_id),
  fund_id uuid references fund_master(fund_id),
  stock_id uuid references stock_master(stock_id),
  transaction_date date not null,
  transaction_type text not null check (transaction_type in ('buy','sell','dividend','fee','transfer_in','transfer_out')),
  units numeric(20,8),
  unit_price numeric(20,8),
  gross_amount numeric(20,2) not null,
  fees numeric(20,2) not null default 0,
  external_reference text unique,
  check (fund_id is not null or stock_id is not null)
);

create table if not exists price_history (
  stock_id uuid not null references stock_master(stock_id),
  price_date date not null,
  close_price numeric(20,8) not null check (close_price >= 0),
  currency char(3) not null default 'INR',
  primary key (stock_id, price_date)
);

create table if not exists risk_metrics (
  portfolio_id uuid not null references portfolio(portfolio_id),
  calculation_date date not null,
  metric_name text not null,
  metric_value numeric(20,8) not null,
  methodology_version text not null,
  primary key (portfolio_id, calculation_date, metric_name, methodology_version)
);

create table if not exists forecast (
  forecast_id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references portfolio(portfolio_id),
  calculation_date date not null,
  horizon_years smallint not null check (horizon_years > 0),
  percentile numeric(5,2) not null check (percentile between 0 and 100),
  projected_value numeric(20,2) not null,
  methodology_version text not null
);

create index if not exists idx_transactions_portfolio_date on transactions(portfolio_id, transaction_date);
create index if not exists idx_fund_nav_date on fund_nav(nav_date desc);
create index if not exists idx_price_history_date on price_history(price_date desc);
