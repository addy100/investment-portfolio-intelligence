import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.main import app
from app.db.database import Base, engine
from database.seed_data import seed_database
from analytics.kpis.returns import calculate_cagr
from analytics.kpis.risk import calculate_sharpe_ratio
import numpy as np

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Ensures database tables are created and seeded before API tests run."""
    Base.metadata.create_all(bind=engine)
    seed_database()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_portfolio_summary_endpoint(client):
    response = client.get("/api/portfolio")
    assert response.status_code == 200
    data = response.json()
    assert "total_value" in data
    assert "xirr" in data

def test_live_market_quotes_endpoint(client):
    response = client.get("/api/market/live-quotes?symbols=RELIANCE,HDFCBANK,NVDA")
    assert response.status_code == 200
    data = response.json()
    assert "quotes" in data
    assert "RELIANCE" in data["quotes"]

def test_zerodha_login_url_endpoint(client):
    response = client.get("/api/zerodha/login-url")
    assert response.status_code == 200
    data = response.json()
    assert "login_url" in data

def test_refresh_database_live_prices(client):
    response = client.post("/api/market/refresh-prices")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"

def test_cagr_math():
    cagr = calculate_cagr(100.0, 144.0, 2.0)
    assert round(cagr, 1) == 20.0
