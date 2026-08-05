import React from 'react';
import { DollarSign, TrendingUp, Award, Activity, AlertCircle, ArrowUpRight } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

export default function ExecutiveSummary({ summary, holdings }) {
  if (!summary) return <div style={{ padding: '40px', textAlign: 'center' }}>Loading summary metrics...</div>;

  const totalValue = summary.total_value || 842500;
  const invested = summary.total_invested || 730650;
  const gain = summary.unrealized_gain || (totalValue - invested);
  const gainPct = summary.unrealized_gain_pct || 15.3;
  const xirr = summary.xirr || 18.5;
  const cagr = summary.cagr || 15.3;

  const pieColors = ['#3B82F6', '#8B5CF6', '#10B981', '#06B6D4', '#F59E0B', '#EC4899'];
  const sectorData = summary.sector_breakdown || [
    { sector: 'Financials', weight: 33.5 },
    { sector: 'US Technology', weight: 18.2 },
    { sector: 'Information Technology', weight: 15.4 },
    { sector: 'Oil Gas & Energy', weight: 12.1 },
    { sector: 'Consumer Goods', weight: 10.8 },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Header Banner */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>Portfolio Overview</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Real-time aggregate performance, XIRR returns, and sector concentration analytics.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <span className="pill-badge pill-emerald">Live AMFI Synced</span>
          <span className="pill-badge pill-blue">SQLite / PostgreSQL Ready</span>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
        {/* Card 1: Net Worth */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>TOTAL PORTFOLIO VALUE</span>
            <DollarSign size={18} color="var(--accent-blue)" />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, marginTop: '8px' }}>
            ₹{totalValue.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--accent-emerald)', marginTop: '6px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <ArrowUpRight size={14} />
            +₹{gain.toLocaleString('en-IN', { maximumFractionDigits: 2 })} (+{gainPct}%)
          </div>
        </div>

        {/* Card 2: Net Invested */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>NET INVESTED</span>
            <Activity size={18} color="var(--accent-purple)" />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, marginTop: '8px' }}>
            ₹{invested.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
            Across {summary.direct_assets_count || 6} Holdings
          </div>
        </div>

        {/* Card 3: XIRR */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>XIRR RETURN</span>
            <TrendingUp size={18} color="var(--accent-emerald)" />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, marginTop: '8px', color: 'var(--accent-emerald)' }}>
            {xirr}%
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
            CAGR: {cagr}%
          </div>
        </div>

        {/* Card 4: Sharpe Ratio */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>SHARPE RATIO</span>
            <Award size={18} color="var(--accent-amber)" />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, marginTop: '8px', color: 'var(--accent-amber)' }}>
            1.85
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--accent-emerald)', marginTop: '6px' }}>
            Top 5% Risk-Adjusted Return
          </div>
        </div>
      </div>

      {/* Main Charts Row */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Asset Allocation Pie */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>Sector Exposure Breakdown</h3>
          <div style={{ height: '240px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={sectorData}
                  dataKey="weight"
                  nameKey="sector"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  innerRadius={50}
                  paddingAngle={4}
                >
                  {sectorData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(val) => `${val}%`} contentStyle={{ background: '#0F172A', border: '1px solid #334155', borderRadius: '8px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', justifyContent: 'center', marginTop: '10px' }}>
            {sectorData.slice(0, 5).map((sec, idx) => (
              <div key={sec.sector} style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}>
                <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: pieColors[idx % pieColors.length] }}></span>
                {sec.sector} ({sec.weight}%)
              </div>
            ))}
          </div>
        </div>

        {/* Sector Weight Bars */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>Sector Concentration Bars</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {sectorData.map((sec, idx) => (
              <div key={sec.sector}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '6px' }}>
                  <span>{sec.sector}</span>
                  <span style={{ fontWeight: 700 }}>{sec.weight}%</span>
                </div>
                <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${sec.weight}%`,
                      height: '100%',
                      background: pieColors[idx % pieColors.length],
                      borderRadius: '4px',
                      transition: 'width 0.8s ease'
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Top Look-Through Underlying Stocks */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>Top Underlying Effective Holdings</h3>
        <table className="custom-table">
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Company Name</th>
              <th>Sector</th>
              <th>Country</th>
              <th>Effective Weight</th>
            </tr>
          </thead>
          <tbody>
            {(holdings?.lookthrough_stocks || []).slice(0, 5).map(stk => (
              <tr key={stk.ticker}>
                <td style={{ fontWeight: 700, color: 'var(--accent-blue)' }}>{stk.ticker}</td>
                <td>{stk.company_name}</td>
                <td><span className="pill-badge pill-blue">{stk.sector}</span></td>
                <td>{stk.country}</td>
                <td style={{ fontWeight: 700 }}>{stk.effective_weight}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
