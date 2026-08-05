# Portfolio Intelligence System Architecture

```
[ Frontend: React + Vite ] 
       │ (REST APIs)
       ▼
[ Backend: FastAPI (Python 3.11) ]
  ├── Analytics Engine (Returns, Risk, Overlap, Monte Carlo)
  ├── Look-Through Stock Exposure Engine
  └── AI Natural Language Processor
       │
       ▼
[ Database: SQLAlchemy 2.0 ORM ]
  ├── SQLite (Local zero-config)
  └── Supabase PostgreSQL (Production ready)
```

## Free Architecture Hosting Plan

- **Frontend**: Deploy static Vite bundle to Cloudflare Pages or GitHub Pages.
- **Backend API**: Deploy FastAPI app to Render (Free Tier web service).
- **Database**: Connect to Supabase PostgreSQL free tier instance via `DATABASE_URL`.
- **Scheduled Refresh**: Trigger GitHub Actions workflow daily to fetch latest AMFI NAVs and update SQLite/PostgreSQL.
