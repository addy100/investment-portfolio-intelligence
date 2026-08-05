import React from 'react';
import { TrendingUp, PieChart, Layers, ShieldAlert, LineChart, Bot, Download, RefreshCw } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onExportExcel }) {
  const navItems = [
    { id: 'summary', label: 'Executive Summary', icon: TrendingUp },
    { id: 'holdings', label: 'Holdings & Look-Through', icon: Layers },
    { id: 'overlap', label: 'Overlap Matrix', icon: PieChart },
    { id: 'risk', label: 'Risk Analytics', icon: ShieldAlert },
    { id: 'forecast', label: 'Monte Carlo Forecast', icon: LineChart },
    { id: 'ai', label: 'AI Assistant', icon: Bot },
  ];

  return (
    <nav style={{
      background: 'rgba(11, 15, 25, 0.85)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid var(--border-light)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      padding: '0 24px'
    }}>
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: '70px'
      }}>
        {/* Brand Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: 'var(--gradient-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 14px 0 rgba(59, 130, 246, 0.4)'
          }}>
            <TrendingUp size={22} color="#ffffff" />
          </div>
          <div>
            <div style={{ fontWeight: 800, fontSize: '1.15rem', letterSpacing: '-0.5px' }}>
              PORTFOLIO<span className="gradient-text">INTELLIGENCE</span>
            </div>
            <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 600 }}>
              DEEP LOOK-THROUGH & FORECAST ENGINE
            </div>
          </div>
        </div>

        {/* Tab Navigation Links */}
        <div style={{ display: 'flex', gap: '6px' }}>
          {navItems.map(item => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                style={{
                  background: isActive ? 'rgba(59, 130, 246, 0.15)' : 'transparent',
                  color: isActive ? 'var(--accent-blue)' : 'var(--text-secondary)',
                  border: isActive ? '1px solid rgba(59, 130, 246, 0.3)' : '1px solid transparent',
                  padding: '8px 16px',
                  borderRadius: '10px',
                  fontWeight: 600,
                  fontSize: '0.85rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  transition: 'all 0.2s ease'
                }}
              >
                <Icon size={16} />
                {item.label}
              </button>
            );
          })}
        </div>

        {/* Export & Status Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button className="btn-secondary" onClick={() => window.location.reload()} title="Refresh Data">
            <RefreshCw size={15} />
          </button>
          <button className="btn-primary" onClick={onExportExcel}>
            <Download size={16} />
            Export Excel
          </button>
        </div>
      </div>
    </nav>
  );
}
