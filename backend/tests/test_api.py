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
    assert data["total_value"] > 0

def test_funds_endpoint(client):
    response = client.get("/api/funds")
    assert response.status_code == 200
    data = response.json()
    assert "funds" in data
    assert len(data["funds"]) >= 3

def test_holdings_lookthrough_endpoint(client):
    response = client.get("/api/holdings")
    assert response.status_code == 200
    data = response.json()
    assert "lookthrough_stocks" in data
    assert "direct_assets" in data

def test_overlap_matrix_endpoint(client):
    response = client.get("/api/overlap")
    assert response.status_code == 200
    data = response.json()
    assert "matrix" in data
    assert "hhi_index" in data

def test_forecast_monte_carlo_endpoint(client):
    response = client.get("/api/forecast?horizon_years=10&monthly_sip=10000")
    assert response.status_code == 200
    data = response.json()
    assert "median_50th" in data
    assert "success_probability" in data

def test_risk_metrics_endpoint(client):
    response = client.get("/api/risk")
    assert response.status_code == 200
    data = response.json()
    assert "sharpe_ratio" in data
    assert "var_95" in data

def test_ai_query_endpoint(client):
    response = client.post("/api/ai/query", json={"question": "How much NVIDIA do I indirectly own?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data

def test_cagr_math():
    cagr = calculate_cagr(100.0, 144.0, 2.0)
    assert round(cagr, 1) == 20.0

def test_sharpe_math():
    returns = np.array([0.01, 0.02, -0.005, 0.015, 0.008])
    sharpe = calculate_sharpe_ratio(returns, 0.06)
    assert isinstance(sharpe, float)
