// src/App.js — ClinicalBot Chat Interface
import React, { useState, useRef, useEffect, useCallback } from 'react';
import axios from 'axios';
import './App.css';

// ── Constants ──────────────────────────────────────────────────────────────
const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const MAX_CHARS = 800;

const SAMPLE_QUESTIONS = [
  { icon: '🧪', text: 'What are the 4 phases of clinical trials?' },
  { icon: '📋', text: 'What is informed consent and why is it important?' },
  { icon: '🛡️', text: 'What is an Institutional Review Board (IRB)?' },
  { icon: '⚠️', text: 'What counts as a serious adverse event (SAE)?' },
  { icon: '🎯', text: 'What is the FDA drug approval process?' },
  { icon: '🔀', text: 'What is randomization and double-blinding?' },
  { icon: '📊', text: 'What are primary vs secondary endpoints?' },
  { icon: '👥', text: 'What does Good Clinical Practice (GCP) require?' },
];

const BADGES = ['RAG Pipeline', 'FAISS Vector DB', 'Gemini AI', 'FastAPI'];

// ── Helpers ────────────────────────────────────────────────────────────────
function formatTime(date) {
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function ConfidenceBadge({ level }) {
  const icons = { high: '✅', medium: '🟡', low: '⚠️', none: '❌' };
  const labels = { high: 'High confidence', medium: 'Medium confidence', low: 'Low confidence', none: 'Error' };
  return (
    <span className={`confidence-badge ${level || 'medium'}`}>
      {icons[level] || '🟡'} {labels[level] || 'Medium confidence'}
    </span>
  );
}

function SourcesPanel({ sources, confidence }) {
  if (!sources || sources.length === 0) return null;
  return (
    <div className="sources-panel">
      <div className="sources-header">
        <span>📚</span> Sources
      </div>
      <div>
        {sources.map((src, i) => (
          <span key={i} className="source-tag">📄 {src}</span>
        ))}
      </div>
      {confidence && <div style={{ marginTop: 8 }}><ConfidenceBadge level={confidence} /></div>}
    </div>
  );
}

function Message({ msg }) {
  const isUser = msg.role === 'user';
  return (
    <div className={`message ${msg.role}`}>
      <div className="message-row">
        <div className={`avatar ${isUser ? 'user-avatar' : 'bot-avatar'}`}>
          {isUser ? '👤' : '🤖'}
        </div>
        <div className={`bubble`}>{msg.content}</div>
      </div>
      <div className="message-meta">{formatTime(msg.time)}</div>
      {!isUser && msg.sources && (
        <SourcesPanel sources={msg.sources} confidence={msg.confidence} />
      )}
    </div>
  );
}

function LoadingMessage() {
  return (
    <div className="message assistant">
      <div className="message-row">
        <div className="avatar bot-avatar">🤖</div>
        <div className="loading-bubble">
          <div className="dot" /><div className="dot" /><div className="dot" />
        </div>
      </div>
    </div>
  );
}

// ── Main App ───────────────────────────────────────────────────────────────
export default function App() {
  const [messages, setMessages]   = useState([]);
  const [input, setInput]         = useState('');
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState('');
  const [apiStatus, setApiStatus] = useState('checking'); // 'online' | 'offline' | 'checking'

  const messagesEndRef = useRef(null);
  const inputRef       = useRef(null);

  // ── Health check ──────────────────────────────────────────
  useEffect(() => {
    const check = async () => {
      try {
        await axios.get(`${API_BASE}/health`, { timeout: 4000 });
        setApiStatus('online');
      } catch {
        setApiStatus('offline');
      }
    };
    check();
    const interval = setInterval(check, 30000);
    return () => clearInterval(interval);
  }, []);

  // ── Auto-scroll ───────────────────────────────────────────
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // ── Send message ──────────────────────────────────────────
  const sendMessage = useCallback(async (questionText) => {
    const question = (questionText || input).trim();
    if (!question || loading) return;

    setError('');
    setInput('');

    const userMsg = { role: 'user', content: question, time: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const { data } = await axios.post(
        `${API_BASE}/chat`,
        { question, top_k: 4 },
        { timeout: 30000 }
      );

      const botMsg = {
        role: 'assistant',
        content: data.answer,
        sources: data.sources,
        confidence: data.confidence,
        time: new Date(),
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      const errText = err.response?.data?.detail
        || (err.code === 'ECONNABORTED' ? 'Request timed out. The backend may be slow to start.' : null)
        || 'Could not connect to the backend. Make sure it is running on port 8000.';
      setError(errText);

      const errMsg = {
        role: 'assistant',
        content: '⚠️ ' + errText,
        time: new Date(),
      };
      setMessages(prev => [...prev, errMsg]);
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [input, loading]);

  // ── Keyboard: Enter to send, Shift+Enter for newline ─────
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  const handleChipClick = (text) => {
    sendMessage(text);
  };

  // ── Render ────────────────────────────────────────────────
  return (
    <div className="app">
      {/* ── Header ── */}
      <header className="header">
        <div className="header-brand">
          <div className="header-logo">🧬</div>
          <div>
            <div className="header-title">ClinicalBot</div>
            <div className="header-subtitle">Clinical Research AI Assistant</div>
          </div>
        </div>

        <div className={`header-status ${apiStatus === 'offline' ? 'offline' : ''}`}>
          <span className="status-dot" />
          {apiStatus === 'online'   && 'Backend Online'}
          {apiStatus === 'offline'  && 'Backend Offline'}
          {apiStatus === 'checking' && 'Connecting…'}
        </div>
      </header>

      {/* ── Body ── */}
      <div className="main-layout">

        {/* Sidebar */}
        <aside className="sidebar">
          <p className="sidebar-section-title">Try asking</p>
          {SAMPLE_QUESTIONS.map((q, i) => (
            <button
              key={i}
              className="sidebar-chip"
              onClick={() => handleChipClick(q.text)}
              disabled={loading}
              id={`sample-q-${i}`}
            >
              <span className="sidebar-chip-icon">{q.icon}</span>
              <span className="sidebar-chip-text">{q.text}</span>
            </button>
          ))}

          <div className="sidebar-divider" />

          <div className="sidebar-info-card">
            <h4>🔬 How it works</h4>
            <p>
              Your question is matched against a clinical knowledge base using FAISS
              vector similarity, then Gemini generates a grounded, sourced answer.
            </p>
          </div>
        </aside>

        {/* Chat Area */}
        <main className="chat-area">
          <div className="messages-container" id="messages-container">

            {messages.length === 0 && !loading ? (
              /* Welcome Screen */
              <div className="welcome-screen">
                <div className="welcome-icon">🧬</div>
                <h1>Clinical Research AI Assistant</h1>
                <p>
                  Ask any question about clinical trials, patient safety, FDA approvals,
                  informed consent, and more — all answers are grounded in the clinical
                  knowledge base via RAG.
                </p>
                <div className="welcome-badges">
                  {BADGES.map(b => (
                    <span key={b} className="badge">✦ {b}</span>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((msg, idx) => <Message key={idx} msg={msg} />)
            )}

            {loading && <LoadingMessage />}
            <div ref={messagesEndRef} />
          </div>

          {/* Error Banner */}
          {error && (
            <div className="error-banner">
              <span>⚠️</span> {error}
              <button
                onClick={() => setError('')}
                style={{ marginLeft: 'auto', background: 'none', border: 'none',
                         color: 'inherit', cursor: 'pointer', fontSize: 14 }}
              >✕</button>
            </div>
          )}

          {/* Input */}
          <div className="input-area">
            <form className="input-form" onSubmit={handleSubmit} id="chat-form">
              <textarea
                ref={inputRef}
                id="question-input"
                className="input-field"
                rows={1}
                value={input}
                onChange={e => setInput(e.target.value.slice(0, MAX_CHARS))}
                onKeyDown={handleKeyDown}
                placeholder="Ask a clinical research question…"
                disabled={loading}
                aria-label="Clinical research question"
              />
              <button
                type="submit"
                id="send-button"
                className="send-btn"
                disabled={loading || !input.trim()}
                aria-label="Send question"
              >
                {loading ? '⏳' : '➤'}
              </button>
            </form>

            <div className="input-footer">
              <span className="input-hint">Enter to send · Shift+Enter for new line</span>
              <span className={`char-count ${input.length > MAX_CHARS * 0.85 ? 'warn' : ''}`}>
                {input.length} / {MAX_CHARS}
              </span>
            </div>
          </div>
        </main>

      </div>
    </div>
  );
}
