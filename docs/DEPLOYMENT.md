# Deployment runbook

## 1. Supabase

1. Create a new Supabase project in the region closest to the portfolio owner.
2. Run `database/migrations/001_initial_schema.sql` in the Supabase SQL Editor.
3. Copy the direct PostgreSQL connection string into Render as `DATABASE_URL`.

The v1 API is read-only and has no authentication. Do not expose Supabase service-role keys in the frontend or GitHub Actions.

## 2. Render API

1. Push this repository to GitHub and create a Render Blueprint from `render.yaml`.
2. Add `DATABASE_URL` and `CORS_ORIGINS` to the service environment. `CORS_ORIGINS` must be the final Pages origin, for example `https://account.github.io`.
3. Confirm `https://<render-service>/health` returns `{"status":"ok",...}`.

## 3. GitHub Pages frontend

1. In GitHub, enable Pages with **GitHub Actions** as the source.
2. Create the repository variable `API_BASE_URL` with the Render service URL, without a trailing slash.
3. Push to `main` or manually run **Deploy frontend**.

The deployment workflow injects this value into the otherwise static `frontend/config.js`; no API secret is used in the browser.

## 4. Scheduled ETL

The weekday workflow currently emits only an ETL heartbeat. Add source-specific secrets only when the corresponding authorized adapter is implemented. A production financial-data refresh should write an as-of date and source URL for every imported observation.
