from datetime import UTC, datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.schemas import ApiMessage, AssetLink, FundSummary, HoldingSummary, PortfolioSummary

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def pending(feature: str) -> ApiMessage:
    return ApiMessage(detail=f"{feature} will be populated after the portfolio import and ETL modules ship.")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "orbit-api"}


@app.get("/portfolio", response_model=PortfolioSummary)
def portfolio() -> PortfolioSummary:
    return PortfolioSummary()


@app.get("/funds", response_model=list[FundSummary])
def funds() -> list[FundSummary]:
    return []


@app.get("/holdings", response_model=list[HoldingSummary])
def holdings() -> list[HoldingSummary]:
    return []


@app.get("/overlap", response_model=ApiMessage)
def overlap() -> ApiMessage:
    return pending("Overlap analytics")


@app.get("/forecast", response_model=ApiMessage)
def forecast() -> ApiMessage:
    return pending("Forecast analytics")


@app.get("/risk", response_model=ApiMessage)
def risk() -> ApiMessage:
    return pending("Risk analytics")


@app.get("/recommendation", response_model=ApiMessage)
def recommendation() -> ApiMessage:
    return pending("Recommendations")


@app.get("/excel", response_model=AssetLink)
def excel() -> AssetLink:
    return AssetLink(
        url=settings.excel_release_url,
        status="available" if settings.excel_release_url else "not_published",
        updated_at=datetime.now(UTC),
    )


@app.get("/powerbi", response_model=AssetLink)
def powerbi() -> AssetLink:
    return AssetLink(
        url=settings.powerbi_template_url,
        status="available" if settings.powerbi_template_url else "not_published",
        updated_at=datetime.now(UTC),
    )
