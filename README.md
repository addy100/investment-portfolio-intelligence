# Portfolio Intelligence Platform

Production-grade, token-efficient, free-architecture financial portfolio intelligence platform. Includes a **FastAPI REST API**, **SQLite / PostgreSQL (Supabase ready)** database schema with automatic seed data, **pure Python financial analytics engine** (KPIs, Look-Through, Overlap matrix, Monte Carlo forecast), **Zerodha Kite & NSE Live Exchange Data**, high-performance **React + Vite visual dashboard**, **Excel workbook generator**, **Power BI schemas**, and **GitHub Actions CI/CD pipeline** for GitHub Pages deployment.

---

## Free Architecture Overview

| Component | Platform / Tech | Cost | Purpose |
| :--- | :--- | :--- | :--- |
| **Source Code** | GitHub | Free | Version control & repository |
| **Frontend** | React + Vite | Free | Glassmorphic responsive web UI (Deployed on GitHub Pages / Cloudflare Pages) |
| **Backend API** | Python (FastAPI + Uvicorn) | Free | High-performance async REST API (Deployable to Render Free Tier) |
| **Database** | SQLite / PostgreSQL (Supabase) | Free | SQLAlchemy 2.0 ORM supporting local zero-config SQLite and production Supabase |
| **Live Market Data** | Zerodha Kite API + NSE Exchange | Free / Native | Real-time stock prices & broker portfolio synchronization |
| **Scheduled Jobs** | GitHub Actions | Free | Automated ETL refresh, daily NAV updates, and unit testing |
| **Excel & Power BI** | OpenPyXL & Power BI Desktop | Free | Dynamic formatted `.xlsx` downloads & dataset schemas |

---

## Key Features

1. **Deep Look-Through Stock Exposure Engine**:
   - Combines direct stock holdings with indirect stock exposures inside Mutual Funds and ETFs.
   - Answers questions like *"What is my total effective exposure to NVIDIA, Reliance, or HDFC Bank?"*

2. **Portfolio Overlap Matrix & Concentration Analytics**:
   - Pairwise overlap heatmap matrix between mutual funds.
   - Common underlying stock holdings count and shared weight contribution.
   - Herfindahl-Hirschman Index (HHI) and Effective Number of Stocks.

3. **Financial Return & Risk Analytics**:
   - **Returns**: XIRR (Newton-Raphson), CAGR, Alpha, Beta, Jensen's Alpha, Information Ratio.
   - **Risk**: Sharpe Ratio, Sortino Ratio, Treynor Ratio, Historical VaR (95%), Conditional VaR (95%), Maximum Drawdown, Volatility, Upside & Downside Capture Ratios.

4. **Stochastic Monte Carlo Wealth Forecast**:
   - 1,000-run simulation over 5, 10, 15+ year horizons.
   - Interactive SIP amount and goal target sliders.
   - Percentile growth outcomes (10th Worst Case, 50th Median, Expected Mean, 90th Best Case, and Goal Achievement Probability).

5. **AI Portfolio Assistant**:
   - Natural language query box answering prompts like *"How much NVIDIA do I indirectly own?"*, *"How much exposure do I have to banking?"*, *"Which fund is dragging returns?"*

6. **Live Exchange Market Data & Zerodha OAuth**:
   - Direct integration with **Zerodha Kite Connect API** for live broker holdings & quotes.
   - Direct **NSE Exchange** live market quotes for all Indian (`.NS`) and US equities.

7. **Multi-Tab Excel & Power BI Exporter**:
   - Generates beautifully formatted, styled `.xlsx` workbooks (`Dashboard`, `Portfolio`, `Funds`, `Stocks`, `Overlap`, `Forecast`, `Risk`, `Settings`).
   - Complete Power BI dataset schema and DAX measures.

---

## Quick Start (Run Locally)

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher (for frontend local development)

---

### Step 1: Clone Repository

```bash
git clone https://github.com/addy100/investment-portfolio-intelligence.git
cd investment-portfolio-intelligence
```

---

### Step 2: Set Up Backend API (FastAPI)

```bash
cd backend

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Launch FastAPI development server
uvicorn app.main:app --reload
```

The REST API will start on **`http://localhost:8000`**.

Interactive API Documentation:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

> Note: On initial startup, the backend automatically creates all SQL database tables (`portfolio.db`) and seeds realistic sample assets, funds, and NAV history!

---

### Step 3: Set Up Frontend Dashboard (React + Vite)

Open a new terminal tab:

```bash
cd investment-portfolio-intelligence/frontend

# Install dependencies
npm install

# Start Vite local development server
npm run dev
```

The Web Application Dashboard will start on **`http://localhost:5173`**.

---

### Step 4: Run Automated Tests

```bash
cd backend
source venv/bin/activate
pytest -v
```

---

## Environment Configuration (`.env`)

Create an optional `.env` file inside the `backend/` directory to configure custom credentials:

```ini
# Database (Defaults to zero-config SQLite)
DATABASE_URL=sqlite:///./portfolio.db

# For Production Supabase PostgreSQL:
# DATABASE_URL=postgresql://postgres:PASSWORD@db.PROJECT.supabase.co:5432/postgres

# Zerodha Kite Connect API Credentials (Optional)
KITE_API_KEY=your_zerodha_api_key
KITE_API_SECRET=your_zerodha_api_secret
KITE_ACCESS_TOKEN=your_zerodha_access_token
```

---

## Live Deployment Setup

### Deploy Frontend to GitHub Pages

1. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Deploy Portfolio Intelligence"
   git push origin main
   ```
2. Go to your repository on GitHub -> **Settings** -> **Pages**.
3. Under **Build and deployment** -> **Source**, select **GitHub Actions**.
4. Your live app will be published to:
   **[https://addy100.github.io/investment-portfolio-intelligence/](https://addy100.github.io/investment-portfolio-intelligence/)**

### Deploy Backend API to Render (Free Tier)

1. Go to [Render Dashboard](https://dashboard.render.com/) -> **New Web Service**.
2. Connect your `investment-portfolio-intelligence` repository.
3. Settings:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## REST API Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/portfolio` | Portfolio valuation, XIRR returns, sector breakdown. |
| `GET` | `/api/funds` | Fund Master list, scheme codes, and expense ratios. |
| `GET` | `/api/holdings` | Direct stocks + deep look-through indirect stock exposures. |
| `GET` | `/api/overlap` | Pairwise mutual fund overlap matrix and shared holdings details. |
| `GET` | `/api/forecast` | Monte Carlo forecast simulation over 5/10/15 year horizons. |
| `GET` | `/api/risk` | Sharpe ratio, Sortino, VaR 95%, Max Drawdown, capture ratios. |
| `GET` | `/api/recommendation` | Portfolio optimization & expense reduction advice. |
| `GET` | `/api/market/live-quotes` | Real-time exchange quotes from NSE / Zerodha. |
| `POST` | `/api/market/refresh-prices` | Updates database with fresh live exchange stock prices. |
| `GET` | `/api/zerodha/login-url` | Official Zerodha Kite OAuth login URL. |
| `POST` | `/api/zerodha/session` | Authenticates Zerodha OAuth request token. |
| `GET` | `/api/excel` | Dynamic Excel binary file download (`.xlsx`). |
| `GET` | `/api/powerbi` | Power BI dataset schema and DAX definitions. |
| `POST` | `/api/ai/query` | Natural language portfolio assistant query endpoint. |

---

## Repository Structure

```
investment-portfolio-intelligence/
├── backend/                  # FastAPI Application & REST Endpoints
│   ├── app/
│   │   ├── api/              # API Route Handlers (Portfolio, Holdings, Overlap, Risk, Forecast, AI, Zerodha, Live Market)
│   │   ├── core/             # Application Configuration & Settings
│   │   ├── db/               # SQLAlchemy Session & DB Connection
│   │   ├── models/           # Database Models (12 Core Tables)
│   │   └── main.py           # App Entrypoint
│   ├── tests/                # Pytest Test Suite
│   └── requirements.txt      # Python Dependencies
├── analytics/                # Financial Analytics Engine
│   ├── kpis/                 # Return (XIRR, CAGR) & Risk (Sharpe, Sortino, VaR)
│   ├── lookthrough.py        # Mutual Fund & ETF Constituent Look-Through Engine
│   ├── overlap.py            # Portfolio Overlap Matrix & HHI Calculation
│   └── forecast.py           # Monte Carlo & Historical Bootstrap Engine
├── etl/                      # Data Importers & Market Data Fetchers
│   ├── fetchers/             # Zerodha Kite & NSE Live Exchange Data Provider
│   ├── parsers/              # Zerodha CSV & CAS Statement Parsers
│   └── pipeline.py           # Automated Daily ETL Refresh Pipeline
├── database/                 # SQL Schema & Data Seeders
│   ├── schema.sql            # PostgreSQL / SQLite DDL Schema
│   └── seed_data.py          # Sample Data Generator
├── frontend/                 # React + Vite Frontend App
│   ├── src/
│   │   ├── components/       # UI Views (Executive Summary, Holdings, Overlap, Risk, Forecast, AI)
│   │   ├── services/         # API Integration Layer
│   │   └── index.css         # Glassmorphic Dark Theme Styling
│   └── package.json
├── excel/                    # Formatted Excel Exporter (`.xlsx`)
├── powerbi/                  # Power BI Dataset Schema & DAX Definitions
├── docs/                     # API, Architecture, & Deployment Documentation
└── .github/workflows/        # GitHub Actions CI/CD Pipeline
```

---

## License
MIT
