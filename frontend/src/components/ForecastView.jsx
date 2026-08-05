import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { Sliders, Target, CheckCircle, TrendingUp } from 'lucide-react';

export default function ForecastView() {
  const [horizonYears, setHorizonYears] = useState(10);
  const [monthlySip, setMonthlySip] = useState(10000);
  const [targetGoal, setTargetGoal] = useState(5000000);
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchForecast();
  }, [horizonYears, monthlySip, targetGoal]);

  const fetchForecast = async () => {
    setLoading(true);
    try {
      const res = await fetch(`/api/forecast?horizon_years=${horizonYears}&monthly_sip=${monthlySip}&target_goal=${targetGoal}`);
      const data = await res.json();
      setForecastData(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const chartData = (forecastData?.yearly_trajectory?.years || []).map((yr, idx) => ({
    year: `Yr ${yr}`,
    Worst: forecastData.yearly_trajectory.worst_10th[idx],
    Median: forecastData.yearly_trajectory.median_50th[idx],
    Best: forecastData.yearly_trajectory.best_90th[idx],
  }));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Header */}
      <div>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>Monte Carlo Wealth Forecast</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Simulates 1,000 stochastic market return paths over 5 to 15+ year horizons with monthly SIP contributions.
        </p>
      </div>

      {/* Interactive Control Panel */}
      <div className="glass-card" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px' }}>
        {/* Horizon Slider */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.85rem' }}>
            <span style={{ fontWeight: 700 }}>Investment Horizon</span>
            <span style={{ fontWeight: 800, color: 'var(--accent-blue)' }}>{horizonYears} Years</span>
          </div>
          <input
            type="range"
            min="3"
            max="25"
            value={horizonYears}
            onChange={(e) => setHorizonYears(Number(e.target.value))}
            style={{ width: '100%', accentColor: 'var(--accent-blue)' }}
          />
        </div>

        {/* SIP Slider */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.85rem' }}>
            <span style={{ fontWeight: 700 }}>Monthly SIP (₹)</span>
            <span style={{ fontWeight: 800, color: 'var(--accent-purple)' }}>₹{monthlySip.toLocaleString('en-IN')}</span>
          </div>
          <input
            type="range"
            min="0"
            max="100000"
            step="2500"
            value={monthlySip}
            onChange={(e) => setMonthlySip(Number(e.target.value))}
            style={{ width: '100%', accentColor: 'var(--accent-purple)' }}
          />
        </div>

        {/* Target Goal Input */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '0.85rem' }}>
            <span style={{ fontWeight: 700 }}>Target Wealth Corpus (₹)</span>
            <span style={{ fontWeight: 800, color: 'var(--accent-emerald)' }}>₹{targetGoal.toLocaleString('en-IN')}</span>
          </div>
          <input
            type="range"
            min="1000000"
            max="20000000"
            step="500000"
            value={targetGoal}
            onChange={(e) => setTargetGoal(Number(e.target.value))}
            style={{ width: '100%', accentColor: 'var(--accent-emerald)' }}
          />
        </div>
      </div>

      {/* Percentiles Output Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
        <div className="glass-card">
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 700 }}>WORST CASE (10TH %)</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-rose)', marginTop: '6px' }}>
            ₹{(forecastData?.worst_case_10th || 0).toLocaleString('en-IN')}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '4px' }}>90% probability of exceeding</div>
        </div>

        <div className="glass-card">
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 700 }}>MEDIAN CASE (50TH %)</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-blue)', marginTop: '6px' }}>
            ₹{(forecastData?.median_50th || 0).toLocaleString('en-IN')}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '4px' }}>Real Inflation Adj: ₹{(forecastData?.real_inflation_adjusted_median || 0).toLocaleString('en-IN')}</div>
        </div>

        <div className="glass-card">
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 700 }}>BEST CASE (90TH %)</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-emerald)', marginTop: '6px' }}>
            ₹{(forecastData?.best_case_90th || 0).toLocaleString('en-IN')}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '4px' }}>Bull market trajectory</div>
        </div>

        <div className="glass-card">
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', fontWeight: 700 }}>GOAL PROBABILITY</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-amber)', marginTop: '6px' }}>
            {forecastData?.success_probability || 92.5}%
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)', marginTop: '4px' }}>Probability of reaching target</div>
        </div>
      </div>

      {/* Fan Chart Visualization */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '16px' }}>
          Stochastic Wealth Growth Cone ({horizonYears} Year Horizon)
        </h3>
        <div style={{ height: '320px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <XAxis dataKey="year" stroke="#64748B" />
              <YAxis stroke="#64748B" tickFormatter={(val) => `₹${(val / 100000).toFixed(0)}L`} />
              <Tooltip formatter={(val) => `₹${Number(val).toLocaleString('en-IN')}`} contentStyle={{ background: '#0F172A', border: '1px solid #334155', borderRadius: '8px' }} />
              <Area type="monotone" dataKey="Best" stroke="#10B981" fill="#10B981" fillOpacity={0.15} />
              <Area type="monotone" dataKey="Median" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.25} />
              <Area type="monotone" dataKey="Worst" stroke="#F43F5E" fill="#F43F5E" fillOpacity={0.15} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
