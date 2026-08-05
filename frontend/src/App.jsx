import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ExecutiveSummary from './components/ExecutiveSummary';
import HoldingsView from './components/HoldingsView';
import OverlapView from './components/OverlapView';
import RiskView from './components/RiskView';
import ForecastView from './components/ForecastView';
import AIAssistant from './components/AIAssistant';

// Client-side fallback data for static GitHub Pages hosting
const fallbackSummary = {
  portfolio_id: 1,
  name: "Wealth Builder Alpha",
  owner: "John Doe",
  total_value: 842500.0,
  total_invested: 730650.0,
  unrealized_gain: 111850.0,
  unrealized_gain_pct: 15.31,
  xirr: 18.5,
  cagr: 15.3,
  direct_assets_count: 6,
  underlying_stocks_count: 12,
  sector_breakdown: [
    { sector: 'Financials', weight: 33.5, value: 282237.5 },
    { sector: 'US Technology', weight: 18.2, value: 153335.0 },
    { sector: 'Information Technology', weight: 15.4, value: 129745.0 },
    { sector: 'Oil Gas & Consumable Fuels', weight: 12.1, value: 101942.5 },
    { sector: 'Consumer Goods', weight: 10.8, value: 90990.0 },
    { sector: 'Healthcare & Pharma', weight: 5.6, value: 47180.0 },
    { sector: 'Automobile', weight: 4.4, value: 37070.0 }
  ]
};

const fallbackHoldings = {
  total_portfolio_value: 842500.0,
  total_invested: 730650.0,
  direct_assets: [
    { asset_type: 'STOCK', symbol: 'RELIANCE', name: 'Reliance Industries Ltd.', units: 50, invested: 122500, current_value: 147500, gain_loss: 25000, gain_loss_pct: 20.41 },
    { asset_type: 'STOCK', symbol: 'HDFCBANK', name: 'HDFC Bank Ltd.', units: 100, invested: 148000, current_value: 162000, gain_loss: 14000, gain_loss_pct: 9.46 },
    { asset_type: 'STOCK', symbol: 'NVDA', name: 'NVIDIA Corporation', units: 80, invested: 56640, current_value: 83000, gain_loss: 26360, gain_loss_pct: 46.54 },
    { asset_type: 'MF', symbol: '120503', name: 'Axis Bluechip Fund Direct Growth', units: 2500, invested: 113000, current_value: 132500, gain_loss: 19500, gain_loss_pct: 17.26 },
    { asset_type: 'MF', symbol: '122639', name: 'Parag Parikh Flexi Cap Fund Direct Growth', units: 3000, invested: 158400, current_value: 184500, gain_loss: 26100, gain_loss_pct: 16.48 },
    { asset_type: 'ETF', symbol: 'NIFTYBEES', name: 'Nippon India ETF Nifty BeES', units: 500, invested: 120000, current_value: 133000, gain_loss: 13000, gain_loss_pct: 10.83 }
  ],
  lookthrough_stocks: [
    { ticker: 'HDFCBANK', company_name: 'HDFC Bank Ltd.', sector: 'Financials', country: 'India', direct_value: 162000, indirect_value: 41250, total_value: 203250, effective_weight: 24.12, sources: [{ source: 'Direct Equity', percentage: 100, value: 162000 }, { source: 'Fund: Axis Bluechip', percentage: 9.1, value: 12057 }, { source: 'Fund: Parag Parikh Flexi Cap', percentage: 8.1, value: 14944.5 }, { source: 'ETF: Nifty BeES', percentage: 11.5, value: 15295 }] },
    { ticker: 'RELIANCE', company_name: 'Reliance Industries Ltd.', sector: 'Oil Gas & Energy', country: 'India', direct_value: 147500, indirect_value: 24430, total_value: 171930, effective_weight: 20.41, sources: [{ source: 'Direct Equity', percentage: 100, value: 147500 }, { source: 'Fund: Axis Bluechip', percentage: 8.2, value: 10865 }, { source: 'ETF: Nifty BeES', percentage: 10.2, value: 13566 }] },
    { ticker: 'NVDA', company_name: 'NVIDIA Corporation', sector: 'US Technology', country: 'USA', direct_value: 83000, indirect_value: 8302.5, total_value: 91302.5, effective_weight: 10.84, sources: [{ source: 'Direct Equity', percentage: 100, value: 83000 }, { source: 'Fund: Parag Parikh Flexi Cap', percentage: 4.5, value: 8302.5 }] },
    { ticker: 'ICICIBANK', company_name: 'ICICI Bank Ltd.', sector: 'Financials', country: 'India', direct_value: 0, indirect_value: 22961, total_value: 22961, effective_weight: 2.73, sources: [{ source: 'Fund: Axis Bluechip', percentage: 9.5, value: 12587.5 }, { source: 'ETF: Nifty BeES', percentage: 7.8, value: 10374 }] },
    { ticker: 'GOOGL', company_name: 'Alphabet Inc.', sector: 'US Technology', country: 'USA', direct_value: 0, indirect_value: 11439, total_value: 11439, effective_weight: 1.36, sources: [{ source: 'Fund: Parag Parikh Flexi Cap', percentage: 6.2, value: 11439 }] },
    { ticker: 'TCS', company_name: 'Tata Consultancy Services Ltd.', sector: 'Information Technology', country: 'India', direct_value: 0, indirect_value: 14728, total_value: 14728, effective_weight: 1.75, sources: [{ source: 'Fund: Axis Bluechip', percentage: 7.0, value: 9275 }, { source: 'ETF: Nifty BeES', percentage: 4.1, value: 5453 }] }
  ]
};

const fallbackOverlap = {
  funds: [
    { scheme_code: '120503', fund_name: 'Axis Bluechip Fund' },
    { scheme_code: '122639', fund_name: 'Parag Parikh Flexi Cap' },
    { scheme_code: '125497', fund_name: 'SBI Small Cap Fund' }
  ],
  matrix: [
    { scheme_code: '120503', fund_name: 'Axis Bluechip Fund', overlaps: [100.0, 18.5, 4.2] },
    { scheme_code: '122639', fund_name: 'Parag Parikh Flexi Cap', overlaps: [18.5, 100.0, 6.8] },
    { scheme_code: '125497', fund_name: 'SBI Small Cap Fund', overlaps: [4.2, 6.8, 100.0] }
  ],
  pairwise_details: [
    {
      fund_a: 'Axis Bluechip Fund',
      fund_b: 'Parag Parikh Flexi Cap',
      overlap_percentage: 18.5,
      common_stocks: 2,
      shared_holdings: [
        { ticker: 'HDFCBANK', weight_fund_a: 9.1, weight_fund_b: 8.1, overlap_weight: 8.1 },
        { ticker: 'ITC', weight_fund_a: 3.5, weight_fund_b: 5.2, overlap_weight: 3.5 }
      ]
    }
  ],
  hhi_index: 840.5,
  effective_num_stocks: 11.9
};

const fallbackRisk = {
  sharpe_ratio: 1.85,
  sortino_ratio: 2.42,
  treynor_ratio: 0.145,
  var_95: -1.85,
  cvar_95: -2.65,
  max_drawdown: -11.4,
  volatility: 12.6,
  beta: 0.92,
  alpha: 4.8,
  tracking_error: 2.1,
  upside_capture: 106.4,
  downside_capture: 84.2
};

export default function App() {
  const [activeTab, setActiveTab] = useState('summary');
  const [summaryData, setSummaryData] = useState(fallbackSummary);
  const [holdingsData, setHoldingsData] = useState(fallbackHoldings);
  const [overlapData, setOverlapData] = useState(fallbackOverlap);
  const [riskData, setRiskData] = useState(fallbackRisk);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      const [sumRes, holdRes, overRes, riskRes] = await Promise.all([
        fetch('/api/portfolio'),
        fetch('/api/holdings'),
        fetch('/api/overlap'),
        fetch('/api/risk')
      ]);

      if (sumRes.ok && holdRes.ok) {
        setSummaryData(await sumRes.json());
        setHoldingsData(await holdRes.json());
        setOverlapData(await overRes.json());
        setRiskData(await riskRes.json());
      }
    } catch (e) {
      console.log("Using interactive client-side fallback metrics for static GitHub Pages host.");
    }
  };

  const handleExportExcel = () => {
    window.open('/api/excel', '_blank');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onExportExcel={handleExportExcel}
      />

      <main style={{
        flex: 1,
        maxWidth: '1400px',
        width: '100%',
        margin: '0 auto',
        padding: '32px 24px'
      }}>
        {activeTab === 'summary' && <ExecutiveSummary summary={summaryData} holdings={holdingsData} />}
        {activeTab === 'holdings' && <HoldingsView holdings={holdingsData} />}
        {activeTab === 'overlap' && <OverlapView overlap={overlapData} />}
        {activeTab === 'risk' && <RiskView risk={riskData} />}
        {activeTab === 'forecast' && <ForecastView />}
        {activeTab === 'ai' && <AIAssistant />}
      </main>

      <footer style={{
        borderTop: '1px solid var(--border-light)',
        padding: '20px 24px',
        textAlign: 'center',
        color: 'var(--text-muted)',
        fontSize: '0.8rem'
      }}>
        Portfolio Intelligence Platform • Free Architecture (FastAPI + React + SQLite/Supabase + GitHub Pages CI/CD)
      </footer>
    </div>
  );
}
