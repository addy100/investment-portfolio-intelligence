import React, { useState } from 'react';
import { Bot, Send, Sparkles, Terminal, CheckCircle2 } from 'lucide-react';

export default function AIAssistant() {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: 'Hello! I am your AI Portfolio Assistant. Ask me anything about your direct equity, indirect fund exposure, overlap, risk metrics, or future wealth projections.',
      sql: null
    }
  ]);
  const [loading, setLoading] = useState(false);

  const samplePrompts = [
    "How much NVIDIA do I indirectly own?",
    "How much exposure do I have to banking?",
    "Which fund is dragging returns?",
    "Suggest a better ETF.",
    "What if I invest ₹10,000/month for 15 years?"
  ];

  const handleSend = async (queryText) => {
    const promptToUse = queryText || question;
    if (!promptToUse.trim()) return;

    const userMsg = { sender: 'user', text: promptToUse };
    setMessages(prev => [...prev, userMsg]);
    setQuestion('');
    setLoading(true);

    try {
      const res = await fetch('/api/ai/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: promptToUse })
      });
      const data = await res.json();
      setMessages(prev => [...prev, {
        sender: 'ai',
        text: data.answer,
        sql: data.sql_used
      }]);
    } catch (e) {
      setMessages(prev => [...prev, {
        sender: 'ai',
        text: "Error processing query. Please check backend connection.",
        sql: null
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '1000px', margin: '0 auto', width: '100%' }}>
      {/* Header */}
      <div>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Bot size={28} color="var(--accent-purple)" />
          AI Portfolio Assistant
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
          Ask natural language questions about your portfolio, underlying stock holdings, and risk metrics.
        </p>
      </div>

      {/* Quick Sample Chips */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
        {samplePrompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(p)}
            style={{
              background: 'rgba(255, 255, 255, 0.04)',
              border: '1px solid var(--border-light)',
              color: 'var(--text-primary)',
              padding: '6px 14px',
              borderRadius: '20px',
              fontSize: '0.8rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.2s ease'
            }}
          >
            <Sparkles size={13} color="var(--accent-cyan)" />
            {p}
          </button>
        ))}
      </div>

      {/* Chat Thread */}
      <div className="glass-card" style={{ minHeight: '400px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', overflowY: 'auto', maxHeight: '480px', paddingRight: '6px' }}>
          {messages.map((m, idx) => (
            <div
              key={idx}
              style={{
                alignSelf: m.sender === 'user' ? 'flex-end' : 'flex-start',
                maxWidth: '85%',
                background: m.sender === 'user' ? 'var(--gradient-primary)' : 'rgba(30, 41, 59, 0.8)',
                border: m.sender === 'ai' ? '1px solid var(--border-light)' : 'none',
                padding: '14px 18px',
                borderRadius: m.sender === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
                fontSize: '0.9rem',
                lineHeight: '1.5'
              }}
            >
              <div>{m.text}</div>
              {m.sql && (
                <div style={{
                  marginTop: '10px',
                  background: '#090D16',
                  padding: '8px 12px',
                  borderRadius: '6px',
                  fontFamily: 'monospace',
                  fontSize: '0.75rem',
                  color: 'var(--accent-cyan)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px'
                }}>
                  <Terminal size={12} />
                  <span>{m.sql}</span>
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic' }}>
              Analyzing database & look-through holdings...
            </div>
          )}
        </div>

        {/* Input Form */}
        <form
          onSubmit={(e) => { e.preventDefault(); handleSend(); }}
          style={{ display: 'flex', gap: '10px', marginTop: '20px' }}
        >
          <input
            type="text"
            placeholder="Ask a question about your portfolio..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            style={{
              flex: 1,
              background: 'rgba(15, 23, 42, 0.9)',
              border: '1px solid var(--border-light)',
              borderRadius: '10px',
              padding: '12px 16px',
              color: '#ffffff',
              fontSize: '0.9rem',
              outline: 'none'
            }}
          />
          <button type="submit" className="btn-primary" disabled={loading}>
            <Send size={16} />
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
