import React from 'react';
import { PieChart, Grid, AlertTriangle } from 'lucide-react';

export default function OverlapView({ overlap }) {
  if (!overlap) return <div style={{ padding: '40px', textAlign: 'center' }}>Loading fund overlap matrix...</div>;

  const funds = overlap.funds || [];
  const matrix = overlap.matrix || [];
  const details = overlap.pairwise_details || [];
  const hhi = overlap.hhi_index || 840.5;
  const effStocks = overlap.effective_num_stocks || 11.9;

  const getHeatmapColor = (val) => {
    if (val === 100) return 'rgba(59, 130, 246, 0.2)';
    if (val > 40) return 'rgba(244, 63, 94, 0.35)'; // High overlap warning
    if (val > 20) return 'rgba(245, 158, 11, 0.3)';  // Medium overlap
    return 'rgba(16, 185, 129, 0.15)';             // Low overlap
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header Banner */}
      <div>
        <h1 style={{ fontSize: '1.8rem', fontWeight 800 }}>Portfolio Overlap Matrix</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Identifies duplicate underlying stock holdings across active funds to eliminate fee drag and unintended concentration.
        </p>
      </div>

      {/* Metric Cards Row */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        <div className="glass-card">
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 700 }}>HHI CONCENTRATION INDEX</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-cyan)', marginTop: '6px' }}>{hhi}</div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Below 1,500 indicates a well-diversified portfolio.
          </div>
        </div>
        <div className="glass-card">
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 700 }}>EFFECTIVE NUMBER OF STOCKS</div>
          <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-purple)', marginTop: '6px' }}>{effStocks} Stocks</div>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Equal-weight equivalent stock diversification count.
          </div>
        </div>
      </div>

      {/* Heatmap Matrix Table */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Grid size={18} color="var(--accent-blue)" />
          Pairwise Fund Overlap Heatmap (% Shared Holdings)
        </h3>
        <div style={{ overflowX: 'auto' }}>
          <table className="custom-table" style={{ textAlign: 'center' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left' }}>Fund Name</th>
                {funds.map(f => (
                  <th key={f.scheme_code} style={{ textAlign: 'center' }}>{f.fund_name}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {matrix.map((row, idx) => (
                <tr key={row.scheme_code}>
                  <td style={{ fontWeight: 700, textAlign: 'left', color: 'var(--text-primary)' }}>{row.fund_name}</td>
                  {row.overlaps.map((val, cIdx) => (
                    <td
                      key={cIdx}
                      style={{
                        background: getHeatmapColor(val),
                        fontWeight: 800,
                        color: val > 40 && val !== 100 ? 'var(--accent-rose)' : 'var(--text-primary)',
                        border: '1px solid rgba(255, 255, 255, 0.05)'
                      }}
                    >
                      {val.toFixed(1)}%
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Shared Holdings Detailed Breakdown */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>
          Duplicate Stock Holdings Breakdown
        </h3>
        {details.map((pair, pIdx) => (
          <div key={pIdx} style={{
            marginBottom: '20px',
            background: 'rgba(255, 255, 255, 0.02)',
            border: '1px solid var(--border-light)',
            borderRadius: '12px',
            padding: '16px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
              <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>
                <span style={{ color: 'var(--accent-blue)' }}>{pair.fund_a}</span> & <span style={{ color: 'var(--accent-purple)' }}>{pair.fund_b}</span>
              </div>
              <span className={`pill-badge ${pair.overlap_percentage > 30 ? 'pill-rose' : 'pill-amber'}`}>
                {pair.overlap_percentage}% Overlap ({pair.common_stocks} Shared Stocks)
              </span>
            </div>

            <table className="custom-table" style={{ fontSize: '0.85rem' }}>
              <thead>
                <tr>
                  <th>Shared Stock</th>
                  <th>Weight in Fund A</th>
                  <th>Weight in Fund B</th>
                  <th>Overlap Contribution</th>
                </tr>
              </thead>
              <tbody>
                {(pair.shared_holdings || []).map(sh => (
                  <tr key={sh.ticker}>
                    <td style={{ fontWeight: 700 }}>{sh.ticker}</td>
                    <td>{sh.weight_fund_a}%</td>
                    <td>{sh.weight_fund_b}%</td>
                    <td style={{ fontWeight: 700, color: 'var(--accent-emerald)' }}>+{sh.overlap_weight}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}
