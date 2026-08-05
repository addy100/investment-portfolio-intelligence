# WebApp GitHub Pages & Free Host Deployment Guide

This guide walks you through deploying the **Portfolio Intelligence Platform** to **GitHub Pages** (Frontend) and **Render / Railway** (Free Python FastAPI Backend).

---

## 1. Deploy Frontend to GitHub Pages (Automatic CI/CD)

The repository includes a pre-configured GitHub Actions workflow in [deploy_gh_pages.yml](file:///Users/heart/.gemini/antigravity/scratch/portfolio-intelligence/.github/workflows/deploy_gh_pages.yml).

### Step 1: Create a New GitHub Repository

```bash
cd /Users/heart/.gemini/antigravity/scratch/portfolio-intelligence
git init
git add .
git commit -m "Initial commit: Portfolio Intelligence Platform"
git branch -M main
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/portfolio-intelligence.git
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub: `https://github.com/<YOUR-GITHUB-USERNAME>/portfolio-intelligence`.
2. Click **Settings** -> **Pages**.
3. Under **Build and deployment**:
   - Source: Select **GitHub Actions**.
4. The workflow will automatically trigger, build the Vite app, and deploy it to:
   `https://<YOUR-GITHUB-USERNAME>.github.io/portfolio-intelligence/`

---

## 2. Deploy Python FastAPI Backend to Render (Free Tier)

Render provides free hosting for Python FastAPI applications.

1. Go to [Render Dashboard](https://dashboard.render.com/) and log in with GitHub.
2. Click **New +** -> **Web Service**.
3. Connect your `portfolio-intelligence` repository.
4. Configure settings:
   - **Name**: `portfolio-intelligence-api`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service**. Your free backend API will be live at `https://portfolio-intelligence-api.onrender.com`.

---

## 3. Database Options (Supabase PostgreSQL or SQLite)

- **Default (SQLite)**: Runs locally and on Render out of the box with zero configuration.
- **Supabase PostgreSQL**: Create a free PostgreSQL database at [Supabase](https://supabase.com), copy the Connection String URI, and add an environment variable in Render:
  `DATABASE_URL=postgresql://postgres:...@db....supabase.co:5432/postgres`

---

## Interactive Features Available on GitHub Pages

The deployed GitHub Pages frontend includes automatic fallback data, so visitors can immediately interact with:
- **Executive Summary Dashboard** (Net worth, XIRR, CAGR, Sector breakdown charts).
- **Holdings Look-Through Table** (Unravelling direct & indirect stock exposure).
- **Pairwise Overlap Heatmap** (Shared holdings & HHI index).
- **Risk Analytics** (Sharpe, Sortino, VaR 95%, Max Drawdown).
- **Monte Carlo Wealth Simulator** (Interactive sliders for horizon & SIP).
- **AI Portfolio Assistant** (Natural language query resolution).
- **Excel & Power BI Exports** (Formatted `.xlsx` generation).
