from fastapi import APIRouter
from app.api.endpoints import (
    portfolio, funds, holdings, overlap,
    forecast, risk, recommendation, exports, ai
)

api_router = APIRouter()

api_router.include_router(portfolio.router, tags=["Portfolio"])
api_router.include_router(funds.router, tags=["Funds"])
api_router.include_router(holdings.router, tags=["Holdings"])
api_router.include_router(overlap.router, tags=["Overlap"])
api_router.include_router(forecast.router, tags=["Forecast"])
api_router.include_router(risk.router, tags=["Risk"])
api_router.include_router(recommendation.router, tags=["Recommendations"])
api_router.include_router(exports.router, tags=["Exports"])
api_router.include_router(ai.router, tags=["AI Assistant"])
