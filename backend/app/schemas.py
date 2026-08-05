from datetime import date, datetime

from pydantic import BaseModel, Field


class ApiMessage(BaseModel):
    status: str = "not_available"
    detail: str


class PortfolioSummary(BaseModel):
    as_of: date | None = None
    total_value: float = 0
    invested_value: float = 0
    xirr: float | None = None
    holdings_count: int = 0


class FundSummary(BaseModel):
    fund_code: str
    name: str
    category: str | None = None
    nav: float | None = None
    nav_date: date | None = None


class HoldingSummary(BaseModel):
    security_id: str
    security_name: str
    asset_type: str
    market_value: float = 0
    weight: float = Field(default=0, ge=0, le=1)


class AssetLink(BaseModel):
    url: str | None = None
    status: str
    updated_at: datetime
