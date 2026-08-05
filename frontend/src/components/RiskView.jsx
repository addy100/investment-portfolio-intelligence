import React from 'react';
import { ShieldAlert, Activity, TrendingDown, ArrowDownRight, ArrowUpRight, Zap } from 'lucide-react';

export default function RiskView({ risk }) {
  const r = risk || {
    sharpe_ratio: 1.85,
    sortino_ratio: 2.42,
    treynor_ratio: 0.145,
    var_95: -1.85,
    cvar_95: -2.65,
    max_drawdown: -11.4,
    volatility: 12.6,
    upside_capture: 106.4,
    downside_capture: 84.2
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>Risk Analytics & Stress Testing</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Comprehensive risk-adjusted metrics, Value at Risk (VaR 95%), downside deviation, and market capture ratios.
        </p>
      </div>

      {/* Main Risk KPIs Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
        {/* Sharpe */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>SHARPE RATIO</span>
            <Activity size={18} color="var(--accent-emerald)" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '8px', color: 'var(--accent-emerald)' }}>
            {r.sharpe_ratio.toFixed(2)}
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Excess return per unit of total risk.
          </div>
        </div>

        {/* Sortino */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>SORTINO RATIO</span>
            <Zap size={18} color="var(--accent-blue)" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '8px', color: 'var(--accent-blue)' }}>
            {r.sortino_ratio.toFixed(2)}
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Excess return per unit of downside risk.
          </div>
        </div>

        {/* VaR 95% */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>VALUE AT RISK (VaR 95%)</span>
            <ShieldAlert size={18} color="var(--accent-rose)" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '8px', color: 'var(--accent-rose)' }}>
            {r.var_95.toFixed(2)}%
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Max expected 1-day portfolio loss (95% confidence).
          </div>
        </div>

        {/* Max Drawdown */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700 }}>MAX DRAWDOWN</span>
            <TrendingDown size={18} color="var(--accent-amber)" />
          </div>
          <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '8px', color: 'var(--accent-amber)' }}>
            {r.max_drawdown.toFixed(2)}%
          </div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Peak-to-trough historical drop.
          </div>
        </div>
      </div>

      {/* Downside & Market Capture Ratios */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div className="glass-card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>Market Capture Ratios</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ background: 'rgba(16, 185, 129, 0.05)', border: '1px solid rgba(16, 185, 129, 0.2)', padding: '16px', borderRadius: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <ArrowUpRight size={18} color="var(--accent-emerald)" />
                  Upside Capture Ratio
                </span>
                <span style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--accent-emerald)' }}>
                  {r.upside_capture.toFixed(1)}%
                </span>
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
                Outperforms benchmark during market rallies (> 100% is desirable).
              </p>
            </div>

            <div style={{ background: 'rgba(59, 130, 246, 0.05)', border: '1px solid rgba(59, 130, 246, 0.2)', padding: '16px', borderRadius: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <ArrowDownRight size={18} color="var(--accent-blue)" />
                  Downside Capture Ratio
                </span>
                <span style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--accent-blue)' }}>
                  {r.downside_capture.toFixed(1)}%
                </span>
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '6px' }}>
                Protects capital during market downturns (&lt; 100% is desirable).
              </p>
            </div>
          </div>
        </div>

        {/* Detailed Risk Breakdown */}
        <div className="glass-card">
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>Risk Parameters Summary</h3>
          <table className="custom-table">
            <tbody>
              <tr>
                <td style={{ color: 'var(--text-secondary)' }}>Annual Volatility (Std Dev)</td>
                <td style={{ fontWeight: 700 }}>{r.volatility.toFixed(2)}%</td>
              </tr>
              <tr>
                <td style={{ color: 'var(--text-secondary)' }}>Conditional VaR (CVaR 95%)</td>
                <td style={{ fontWeight: 700, color: 'var(--accent-rose)' }}>{r.cvar_95.toFixed(2)}%</td>
              </tr>
              <tr>
                <td style={{ color: 'var(--text-secondary)' }}>Beta vs Nifty 50</td>
                <td style={{ fontWeight: 700 }}>0.92</td>
              </tr>
              <tr>
                <td style={{ color: 'var(--text-secondary)' }}>Alpha (Annualized Excess)</td>
                <td style={{ fontWeight: 700, color: 'var(--accent-emerald)' }}>+4.8%</td>
              </tr>
              <tr>
                <td style={{ color: 'var(--text-secondary)' }}>Tracking Error</td>
                <td style={{ fontWeight: 700 }}>2.1%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
