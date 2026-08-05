import React, { useState } from 'react';
import { Layers, ChevronDown, ChevronRight, Eye } from 'lucide-react';

export default function HoldingsView({ holdings }) {
  const [expandedRow, setExpandedRow] = useState(null);

  if (!holdings) return <div style={{ padding: '40px', textAlign: 'center' }}>Loading holdings look-through data...</div>;

  const stocks = holdings.lookthrough_stocks || [];
  const directAssets = holdings.direct_assets || [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Banner */}
      <div>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>Deep Look-Through Holdings</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Unravels Mutual Funds & ETFs to show your total effective direct + indirect stock exposure.
        </p>
      </div>

      {/* Direct Portfolio Assets Table */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Layers size={18} color="var(--accent-blue)" />
          Direct Portfolio Holdings (Stocks, Funds & ETFs)
        </h3>
        <table className="custom-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Symbol</th>
              <th>Asset Name</th>
              <th>Units</th>
              <th>Invested (₹)</th>
              <th>Current Value (₹)</th>
              <th>Gain / Loss</th>
            </tr>
          </thead>
          <tbody>
            {directAssets.map(asset => (
              <tr key={`${asset.asset_type}-${asset.symbol}`}>
                <td>
                  <span className={`pill-badge ${asset.asset_type === 'STOCK' ? 'pill-blue' : asset.asset_type === 'MF' ? 'pill-emerald' : 'pill-amber'}`}>
                    {asset.asset_type}
                  </span>
                </td>
                <td style={{ fontWeight: 700 }}>{asset.symbol}</td>
                <td>{asset.name}</td>
                <td>{asset.units.toLocaleString()}</td>
                <td>₹{asset.invested.toLocaleString('en-IN')}</td>
                <td style={{ fontWeight: 700 }}>₹{asset.current_value.toLocaleString('en-IN')}</td>
                <td style={{ color: asset.gain_loss >= 0 ? 'var(--accent-emerald)' : 'var(--accent-rose)', fontWeight: 700 }}>
                  {asset.gain_loss >= 0 ? '+' : ''}₹{asset.gain_loss.toLocaleString('en-IN')} ({asset.gain_loss_pct.toFixed(2)}%)
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Unravelled Look-Through Stock Exposures Table */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>
          Effective Look-Through Stock Exposure (Direct + Indirect Ownership)
        </h3>
        <table className="custom-table">
          <thead>
            <tr>
              <th style={{ width: '40px' }}></th>
              <th>Stock Ticker</th>
              <th>Company Name</th>
              <th>Sector</th>
              <th>Direct Val (₹)</th>
              <th>Indirect Val (₹)</th>
              <th>Total Exposure (₹)</th>
              <th>Effective Weight</th>
            </tr>
          </thead>
          <tbody>
            {stocks.map(stk => {
              const isExpanded = expandedRow === stk.ticker;
              return (
                <React.Fragment key={stk.ticker}>
                  <tr style={{ cursor: 'pointer' }} onClick={() => setExpandedRow(isExpanded ? null : stk.ticker)}>
                    <td>
                      {isExpanded ? <ChevronDown size={16} color="var(--accent-blue)" /> : <ChevronRight size={16} color="var(--text-muted)" />}
                    </td>
                    <td style={{ fontWeight: 700, color: 'var(--accent-blue)' }}>{stk.ticker}</td>
                    <td>{stk.company_name}</td>
                    <td><span className="pill-badge pill-blue">{stk.sector}</span></td>
                    <td>₹{stk.direct_value.toLocaleString('en-IN')}</td>
                    <td style={{ color: 'var(--accent-purple)', fontWeight: 600 }}>₹{stk.indirect_value.toLocaleString('en-IN')}</td>
                    <td style={{ fontWeight: 800 }}>₹{stk.total_value.toLocaleString('en-IN')}</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ width: '60px', height: '6px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                          <div style={{ width: `${Math.min(stk.effective_weight * 5, 100)}%`, height: '100%', background: 'var(--gradient-primary)' }} />
                        </div>
                        <span style={{ fontWeight: 700 }}>{stk.effective_weight}%</span>
                      </div>
                    </td>
                  </tr>

                  {/* Expanded Sources Drawer */}
                  {isExpanded && (
                    <tr>
                      <td colSpan={8} style={{ background: 'rgba(15, 23, 42, 0.95)', padding: '16px 24px' }}>
                        <div style={{ fontSize: '0.85rem', fontWeight: 700, marginBottom: '8px', color: 'var(--accent-cyan)' }}>
                          Sources of Exposure for {stk.company_name} ({stk.ticker}):
                        </div>
                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px' }}>
                          {(stk.sources || []).map((src, idx) => (
                            <div key={idx} style={{
                              background: 'rgba(255, 255, 255, 0.04)',
                              border: '1px solid var(--border-light)',
                              padding: '8px 14px',
                              borderRadius: '8px',
                              fontSize: '0.8rem'
                            }}>
                              <span style={{ color: 'var(--text-secondary)' }}>{src.source}: </span>
                              <strong style={{ color: 'var(--text-primary)' }}>{src.percentage}% holding</strong> (₹{src.value.toLocaleString('en-IN')})
                            </div>
                          ))}
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
