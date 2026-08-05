# Orbit

Orbit is an open, modular personal-portfolio intelligence platform. Sprint 1 supplies the deployable foundation: a FastAPI service, PostgreSQL schema, static dashboard shell, CI workflows, and an Excel-ready export contract.

## Architecture

```text
browser (GitHub Pages / Cloudflare Pages)
        | HTTPS
FastAPI on Render  <--- GitHub Actions scheduled ETL
        |
Supabase PostgreSQL
        |
Excel / Power BI downloads
```

The frontend is deliberately static. Set `window.PORTFOLIO_API_BASE_URL` in `frontend/config.js` during deployment to point it at the separately hosted API.

## Local development

1. Create a PostgreSQL database and set `DATABASE_URL` (a SQLite URL is also supported for a quick local smoke test).
2. Install the backend package: `pip install -e "./backend[dev]"`.
3. Apply the initial schema: `psql "$DATABASE_URL" -f database/migrations/001_initial_schema.sql`.
4. Start the API: `uvicorn app.main:app --app-dir backend --reload`.
5. Serve `frontend/` with any static-file server.

## API contract (Sprint 1)

`GET /health`, `/portfolio`, `/funds`, `/holdings`, `/overlap`, `/forecast`, `/risk`, `/recommendation`, `/excel`, and `/powerbi` are stable public read endpoints. Responses are empty-but-valid until Sprint 2 ETL begins populating the database.

## Project map

- `backend/` — API and domain services
- `database/` — versioned PostgreSQL schema
- `etl/` — scheduled refresh entry point
- `frontend/` — static dashboard deployed independently
- `excel/` — workbook specification and export contract
- `powerbi/` — data-model guide
- `.github/workflows/` — CI, frontend publishing, scheduled ETL

## Deployment variables

| Variable | Used by | Purpose |
| --- | --- | --- |
| `DATABASE_URL` | API and ETL | Supabase PostgreSQL connection string |
| `CORS_ORIGINS` | API | Comma-separated public frontend origins |
| `EXCEL_RELEASE_URL` | API | Published workbook asset URL (optional) |
| `POWERBI_TEMPLATE_URL` | API | Published Power BI template URL (optional) |

Never commit broker credentials, portfolio exports, or database URLs. Zerodha integration will be added as a user-authorized Sprint 2 module.

See [the deployment runbook](docs/DEPLOYMENT.md) for the one-time Supabase, Render, and GitHub Pages setup.
