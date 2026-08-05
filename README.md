# Portfolio Intelligence Platform

Production-grade, token-efficient, free-architecture financial portfolio intelligence platform. Includes a FastAPI REST API, SQL database schema with automatic seed data, pure Python analytics engine (KPIs, Look-Through stock analysis, Overlap matrix, Monte Carlo forecast), high-performance React/Vite dashboard UI, Excel workbook generator, Power BI schemas, and GitHub Actions CI/CD.

## Free Architecture Overview

| Component | Platform / Tech | Cost | Purpose |
| :--- | :--- | :--- | :--- |
| **Source Code** | GitHub | Free | Version control & repository |
| **Frontend** | React + Vite | Free | Glassmorphic responsive web UI (Deployable to GitHub Pages / Cloudflare Pages) |
| **Backend API** | Python (FastAPI + Uvicorn) | Free | High-performance async REST API (Deployable to Render Free Tier) |
| **Database** | SQLite / PostgreSQL (Supabase) | Free | SQLAlchemy 2.0 ORM supporting local zero-config SQLite and Supabase PostgreSQL |
| **Scheduled Jobs** | GitHub Actions | Free | Automated ETL refresh, data validation, and testing |
| **Excel & Power BI** | OpenPyXL & Power BI Desktop | Free | Dynamic formatted `.xlsx` downloads & dataset schemas |

## Project Structure

```
portfolio-intelligence/
├── backend/                  # FastAPI Application & REST Endpoints
│   ├── app/
│   │   ├── api/              # API Route Handlers
│   │   ├── core/             # Application Configurations
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
├── etl/                      # Data Importers & Parsers
│   ├── parsers/              # Zerodha CSV & CAS Statement Parsers
│   └── pipeline.py           # Automated ETL Refresh Pipeline
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
├── docs/                     # API & Architecture Docs
└── .github/workflows/        # GitHub Actions CI/CD Pipeline
```

## Quick Start (Local Development)

### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run backend API server (starts on http://localhost:8000)
uvicorn app.main:app --reload
```

Interactive API Documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Dashboard UI will be available at `http://localhost:5173`.

### 3. Run Automated Tests

```bash
cd backend
pytest -v
```

## License
MIT
