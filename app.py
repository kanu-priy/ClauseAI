"""
ClauseAI — Multi-Agent Contract Intelligence Platform
Streamlit frontend: parallel agents, risk dashboard, Q&A chat, report export.
"""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from datetime import datetime

from utils.document_loader import load_contract, get_word_count
from utils.helpers import (
    build_full_report, build_plain_text_report,
    SECTION_LABELS, format_file_size
)
from core.graph_builder import run_analysis_parallel
from agents.qa_agent import ask_contract
from core.coordinator import classify_contract

# ─── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="ClauseAI – Contract Intelligence",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
[data-testid="stAppViewContainer"] { background: #f0f4f8; font-family: 'Inter', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1526 0%, #162032 55%, #1a2d44 100%) !important;
    border-right: 1px solid rgba(94,234,212,0.1);
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.6) !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #5eead4 !important; font-size: 10.5px !important; font-weight: 700 !important;
    letter-spacing: 1.4px !important; text-transform: uppercase !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.07) !important; }
[data-testid="stSidebar"] label { color: rgba(255,255,255,0.72) !important; font-size: 13px !important; }

.sb-brand { display:flex; align-items:center; gap:12px; padding:4px 0 18px; }
.sb-icon  { width:42px; height:42px; background:linear-gradient(135deg,#0d9488,#14b8a6);
            border-radius:11px; display:flex; align-items:center; justify-content:center;
            font-size:22px; box-shadow:0 4px 16px rgba(13,148,136,0.35); flex-shrink:0; }
.sb-name  { color:#fff !important; font-size:16px !important; font-weight:700 !important; display:block; }
.sb-sub   { color:rgba(255,255,255,0.38) !important; font-size:9.5px !important; font-weight:600;
            letter-spacing:1.2px; text-transform:uppercase; display:block; margin-top:2px; }

/* Typography */
h1 { font-family:'Playfair Display',serif !important; font-weight:700 !important;
     font-size:2.05rem !important; color:#0c1526 !important; letter-spacing:-0.7px; line-height:1.18; }
h2 { font-family:'Inter',sans-serif !important; font-weight:700 !important;
     font-size:1.25rem !important; color:#0c1526 !important; letter-spacing:-0.3px; }
p, li { color:#4b5675; font-size:13.5px; line-height:1.65; }

/* Metric cards */
[data-testid="stMetric"] {
    background:#fff !important; border:1px solid #e2e8f0 !important;
    border-radius:14px !important; padding:16px 20px !important;
    box-shadow:0 1px 4px rgba(0,0,0,0.05) !important; transition:border-color 0.2s,box-shadow 0.2s !important;
}
[data-testid="stMetric"]:hover { border-color:#0d9488 !important; box-shadow:0 4px 16px rgba(13,148,136,0.1) !important; }
[data-testid="stMetricLabel"] { color:#94a3b8 !important; font-size:10.5px !important;
    font-weight:700 !important; text-transform:uppercase !important; letter-spacing:0.9px !important; }
[data-testid="stMetricValue"] { color:#0c1526 !important; font-size:21px !important; font-weight:700 !important; }

/* Buttons */
.stButton > button {
    background:linear-gradient(135deg,#0d9488,#14b8a6) !important; color:#fff !important;
    border:none !important; border-radius:10px !important; font-weight:600 !important;
    font-size:14px !important; padding:11px 24px !important; font-family:'Inter',sans-serif !important;
    transition:transform 0.15s,box-shadow 0.15s !important; box-shadow:0 4px 14px rgba(13,148,136,0.25) !important;
}
.stButton > button:hover { transform:translateY(-1px) !important; box-shadow:0 6px 20px rgba(13,148,136,0.32) !important; }
.stDownloadButton > button {
    background:#fff !important; color:#0d9488 !important; border:1.5px solid #0d9488 !important;
    border-radius:10px !important; font-weight:600 !important; font-size:13px !important;
    font-family:'Inter',sans-serif !important; transition:background 0.15s !important;
}
.stDownloadButton > button:hover { background:#f0fdfa !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background:#fff !important; border-radius:12px !important; gap:2px; padding:4px;
    border:1px solid #e2e8f0 !important; box-shadow:0 1px 4px rgba(0,0,0,0.04) !important;
}
.stTabs [data-baseweb="tab"] {
    background:transparent !important; color:#64748b !important; border-radius:8px !important;
    font-size:12.5px !important; font-family:'Inter',sans-serif !important;
    font-weight:600 !important; padding:7px 14px !important;
}
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,rgba(13,148,136,0.1),rgba(13,148,136,0.05)) !important;
    color:#0d9488 !important; border:1px solid rgba(13,148,136,0.2) !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background:#fff !important; border:1px solid #e2e8f0 !important; border-radius:14px !important;
    box-shadow:0 1px 4px rgba(0,0,0,0.04) !important; margin-bottom:10px !important;
    transition:border-color 0.2s,box-shadow 0.2s !important;
}
[data-testid="stExpander"]:hover { border-color:rgba(13,148,136,0.35) !important; }
[data-testid="stExpander"] summary { color:#0c1526 !important; font-weight:600 !important;
    font-size:13.5px !important; padding:14px 18px !important; }

/* File uploader */
[data-testid="stFileUploader"] {
    background:#fff !important; border:2px dashed #cbd5e1 !important;
    border-radius:14px !important; padding:10px !important; transition:all 0.2s !important;
}
[data-testid="stFileUploader"]:hover { border-color:#0d9488 !important; background:#f0fdfa !important; }

/* Chat */
.stChatInput > div { background:#fff !important; border:1.5px solid #e2e8f0 !important;
    border-radius:12px !important; transition:border-color 0.2s,box-shadow 0.2s !important; }
.stChatInput > div:focus-within { border-color:#0d9488 !important; box-shadow:0 0 0 3px rgba(13,148,136,0.08) !important; }
[data-testid="stChatMessage"] { background:#fff !important; border:1px solid #e2e8f0 !important;
    border-radius:12px !important; padding:14px !important; margin-bottom:10px !important; }

[data-testid="stAlert"] { border-radius:12px !important; font-size:13.5px !important; }
hr { border-color:#e2e8f0 !important; }

/* Custom components */
.overline { font-size:10px; font-weight:700; letter-spacing:1.4px; text-transform:uppercase;
    color:#94a3b8; margin-bottom:14px; margin-top:2px; }
.risk-card { background:#fff; border:1px solid #e2e8f0; border-radius:16px; padding:24px;
    margin-bottom:18px; box-shadow:0 2px 8px rgba(0,0,0,0.05); }
.ring-wrap { display:flex; align-items:center; gap:22px; margin-bottom:22px; }
.ring-box  { position:relative; width:96px; height:96px; flex-shrink:0; }
.ring-box svg { transform:rotate(-90deg); }
.ring-lbl  { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); text-align:center; line-height:1; }
.ring-num  { font-size:26px; font-weight:700; color:#0c1526; }
.ring-den  { font-size:11px; color:#94a3b8; font-weight:600; margin-top:1px; }
.score-row { display:flex; align-items:center; gap:14px; margin-bottom:11px; }
.score-lbl { width:100px; font-size:12.5px; font-weight:600; color:#4b5675; }
.bar-bg    { flex:1; height:8px; background:#f1f5f9; border-radius:99px; overflow:hidden; }
.bar-fill  { height:100%; border-radius:99px; }
.bar-green { background:linear-gradient(90deg,#059669,#10b981); }
.bar-amber { background:linear-gradient(90deg,#d97706,#f59e0b); }
.bar-red   { background:linear-gradient(90deg,#dc2626,#ef4444); }
.score-num { font-size:13px; font-weight:700; color:#0c1526; width:28px; text-align:right; }
.risk-badge { display:inline-flex; align-items:center; gap:6px; padding:5px 14px;
    border-radius:20px; font-size:12px; font-weight:700; margin-top:8px; }
.rb-low      { background:#ecfdf5; color:#065f46; border:1px solid rgba(6,95,70,0.18); }
.rb-medium   { background:#fffbeb; color:#78350f; border:1px solid rgba(120,53,15,0.18); }
.rb-high     { background:#fef3c7; color:#92400e; border:1px solid rgba(146,64,14,0.18); }
.rb-critical { background:#fee2e2; color:#7f1d1d; border:1px solid rgba(127,29,29,0.18); }
.badge { display:inline-block; padding:3px 9px; border-radius:7px; font-size:10.5px;
    font-weight:700; letter-spacing:0.5px; text-transform:uppercase; white-space:nowrap; }
.b-critical { background:#fee2e2; color:#7f1d1d; }
.b-high     { background:#fef3c7; color:#78350f; }
.b-medium   { background:#dbeafe; color:#1e40af; }
.b-low      { background:#ecfdf5; color:#065f46; }
.rf-item { display:flex; gap:12px; align-items:flex-start; padding:12px 0; border-bottom:1px solid #f1f5f9; }
.rf-item:last-child { border-bottom:none; padding-bottom:0; }
.rf-title { font-size:13px; font-weight:700; color:#0c1526; margin-bottom:3px; }
.pill { display:inline-flex; align-items:center; gap:5px; padding:4px 11px;
    border-radius:20px; font-size:11.5px; font-weight:600; margin:3px; }
.pill-run  { background:#fffbeb; color:#78350f; }
.pill-done { background:#ecfdf5; color:#065f46; }
.feat-card { background:#fff; border:1px solid #e2e8f0; border-radius:16px; padding:22px;
    height:100%; transition:transform 0.2s,box-shadow 0.2s,border-color 0.2s;
    box-shadow:0 2px 6px rgba(0,0,0,0.04); }
.feat-card:hover { border-color:#0d9488; box-shadow:0 8px 24px rgba(13,148,136,0.12); transform:translateY(-3px); }
.feat-icon  { font-size:26px; margin-bottom:10px; }
.feat-title { font-size:14px; font-weight:700; color:#0c1526; margin-bottom:6px; }
.feat-desc  { font-size:12.5px; color:#64748b; line-height:1.6; }
.hero-card  { background:linear-gradient(135deg,#f0fdfa,#e6fffa);
    border:1px solid rgba(13,148,136,0.2); border-radius:16px; padding:22px; }
.hero-card-title { font-size:12px; font-weight:700; color:#0d9488; margin-bottom:10px; }
.hero-step { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.step-num  { width:22px; height:22px; border-radius:50%; background:#0d9488; color:#fff;
    font-size:10px; font-weight:700; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.step-txt  { font-size:12.5px; color:#0c1526; font-weight:500; }
.recent-item { display:flex; align-items:center; gap:12px; padding:9px 0; border-bottom:1px solid #f1f5f9; }
.recent-item:last-child { border-bottom:none; }
.recent-info { flex:1; }
.recent-name { font-size:12.5px; font-weight:600; color:#0c1526; }
.recent-date { font-size:11px; color:#94a3b8; }
.done-chip { font-size:10px; font-weight:700; color:#0d9488; background:#f0fdfa;
    padding:2px 8px; border-radius:5px; text-transform:uppercase; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────
_DEFAULTS = {
    "contract_text": "", "filename": "", "contract_type": "",
    "analysis_results": {}, "risk_result": None,
    "chat_history": [], "analysis_done": False, "word_count": 0,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─── Pure Helpers ──────────────────────────────────────────────
def bar_class(score: int) -> str:
    if score <= 3:   return "bar-green"
    elif score <= 6: return "bar-amber"
    return "bar-red"

def risk_badge(score: int) -> tuple:
    if score <= 3:   return "rb-low",      "✓ Low Risk"
    elif score <= 5: return "rb-medium",   "⚠ Medium Risk"
    elif score <= 7: return "rb-high",     "▲ High Risk"
    return "rb-critical", "🔴 Critical Risk"

def ring_color(score: int) -> str:
    if score <= 3:   return "#059669"
    elif score <= 5: return "#d97706"
    elif score <= 7: return "#f59e0b"
    return "#dc2626"

def safe_ctx(results: dict) -> dict:
    """Build Q&A context — all values guaranteed to be str."""
    ctx = {}
    for k, v in results.items():
        if isinstance(v, str):
            ctx[k] = v[:600]
        elif isinstance(v, dict):
            ctx[k] = v.get("narrative", str(v))[:600]
        else:
            ctx[k] = str(v)[:600]
    return ctx

# ─── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-icon">📋</div>
        <div><span class="sb-name">ClauseAI</span><span class="sb-sub">Enterprise Platform</span></div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("### Workspace")
    st.markdown("Dashboard · Reviews · Risk")
    st.divider()
    st.markdown("### Analysis Modules")
    st.caption("Choose which agents to run:")
    run_legal      = st.checkbox("⚖️  Legal Review",       value=True)
    run_compliance = st.checkbox("🛡️  Compliance Check",   value=True)
    run_finance    = st.checkbox("📈  Financial Risk",      value=True)
    run_operations = st.checkbox("⚙️  Operations Review",  value=True)
    run_risk       = st.checkbox("🚨  Risk Scoring",        value=True)
    run_summary    = st.checkbox("📄  Executive Summary",   value=True)
    run_simplifier = st.checkbox("💬  Clause Simplifier",  value=False,
                                  help="Plain English translation. Adds ~20s.")
    st.divider()
    st.markdown("### Settings")
    show_word_count = st.checkbox("Show word count",       value=True)
    auto_expand     = st.checkbox("Auto-expand sections",  value=False)
    st.divider()
    st.markdown("### About")
    st.markdown("Powered by **Gemini 2.5 Flash** via LangChain.  \nMulti-agent with **LangGraph**.  \n**Supports:** PDF · DOCX · TXT")
    if st.session_state.analysis_done:
        st.divider()
        st.success(f"✅ {st.session_state.filename}")
        if st.session_state.contract_type:
            st.markdown(f'<span style="background:#f0fdfa;color:#0d9488;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:700;">{st.session_state.contract_type}</span>', unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;">
        <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#0d9488,#14b8a6);
             display:flex;align-items:center;justify-content:center;color:#fff;font-size:11px;font-weight:700;flex-shrink:0;">CA</div>
        <div><div style="color:#fff;font-size:12px;font-weight:600;">ClauseAI User</div>
             <div style="color:rgba(255,255,255,0.38);font-size:10px;">Legal Analyst</div></div>
    </div>
    """, unsafe_allow_html=True)

# ─── Topbar ────────────────────────────────────────────────────
enabled_count = sum([run_legal, run_compliance, run_finance,
                     run_operations, run_risk, run_summary, run_simplifier])
bc_col, mod_col = st.columns([3, 1])
with bc_col:
    lbl = st.session_state.filename or "New Review"
    short = lbl if len(lbl) < 42 else lbl[:40] + "…"
    st.markdown(f'<p style="font-size:12px;color:#94a3b8;margin:0;padding:6px 0 0;">Dashboard / <span style="color:#0c1526;font-weight:600;">{short}</span></p>', unsafe_allow_html=True)
with mod_col:
    st.markdown(f'<div style="text-align:right;padding-top:6px;"><span style="background:#f0fdfa;color:#0d9488;padding:4px 13px;border-radius:20px;font-size:11.5px;font-weight:700;border:1px solid rgba(13,148,136,0.25);">{enabled_count} modules active</span></div>', unsafe_allow_html=True)
st.divider()

# ─── Header ────────────────────────────────────────────────────
hdr_col, info_col = st.columns([5, 3], gap="large")
with hdr_col:
    st.markdown('<p style="font-size:10px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#0d9488;margin-bottom:2px;">Contract Intelligence</p>', unsafe_allow_html=True)
    st.title("Contract Review Made Simple")
    st.markdown("Upload your agreement and get comprehensive legal, financial, compliance, and operational insights — powered by 7 specialised AI agents running in parallel.")
with info_col:
    st.markdown("""
    <div class="hero-card">
        <div class="hero-card-title">HOW IT WORKS</div>
        <div class="hero-step"><div class="step-num">1</div><div class="step-txt">Upload a PDF, DOCX, or TXT contract</div></div>
        <div class="hero-step"><div class="step-num">2</div><div class="step-txt">Select analysis modules in the sidebar</div></div>
        <div class="hero-step"><div class="step-num">3</div><div class="step-txt">7 AI agents analyse in parallel</div></div>
        <div class="hero-step"><div class="step-num">4</div><div class="step-txt">Get risk scores, insights &amp; report</div></div>
        <div class="hero-step"><div class="step-num">5</div><div class="step-txt">Ask follow-up questions via chat</div></div>
    </div>
    """, unsafe_allow_html=True)
st.divider()

# ─── File Upload ───────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload Contract", type=["pdf", "docx", "txt"],
    help="PDF, DOCX, or TXT — up to 10 MB",
)

if uploaded_file:
    c1, c2, c3, c4 = st.columns(4)
    n = uploaded_file.name
    raw_type = uploaded_file.type or ""
    fmt = "PDF" if "pdf" in raw_type else ("DOCX" if "word" in raw_type or "docx" in raw_type else "TXT")
    with c1: st.metric("Document", (n[:20]+"…") if len(n)>20 else n)
    with c2: st.metric("Format", fmt)
    with c3: st.metric("Size", format_file_size(uploaded_file.size))
    with c4: st.metric("Uploaded", datetime.now().strftime("%b %d, %Y"))
    st.markdown("---")

    # Build enabled agents list (List[str]) — correct type for run_analysis_parallel
    enabled_agents = [k for k, v in {
        "legal": run_legal, "compliance": run_compliance, "finance": run_finance,
        "operations": run_operations, "risk": run_risk,
        "summary": run_summary, "simplifier": run_simplifier,
    }.items() if v]

    btn_col, tip_col = st.columns([1, 3])
    with btn_col:
        run_clicked = st.button("▶  Run Full Analysis", use_container_width=True)
    with tip_col:
        if not enabled_agents:
            st.warning("⚠ Enable at least one module in the sidebar.")

    if run_clicked and enabled_agents:
        # Reset prior state
        for k in ["analysis_done","analysis_results","risk_result","chat_history","word_count"]:
            st.session_state[k] = _DEFAULTS.get(k)

        with st.spinner("Loading document…"):
            try:
                contract_text = load_contract(uploaded_file)
                st.session_state.contract_text = contract_text
                st.session_state.filename      = uploaded_file.name
                st.session_state.contract_type = classify_contract(contract_text)
            except Exception as e:
                st.error(f"❌ Could not load document: {e}")
                st.stop()

        if show_word_count:
            wc = get_word_count(contract_text)
            st.session_state.word_count = wc
            st.info(f"Document loaded — **{wc:,}** words · Detected: **{st.session_state.contract_type}**")

        MODULE_LABELS = {
            "legal":"Legal","compliance":"Compliance","finance":"Financial",
            "operations":"Operations","risk":"Risk Score","summary":"Summary","simplifier":"Simplifier",
        }
        pills = "".join(f'<span class="pill pill-run">⏳ {MODULE_LABELS[k]}</span>' for k in enabled_agents)
        st.markdown(f"<div style='margin:10px 0 14px;'>{pills}</div>", unsafe_allow_html=True)

        # Single call — passes List[str], correct signature
        with st.spinner("Analysing contract across all active modules…"):
            try:
                results, risk_result = run_analysis_parallel(contract_text, enabled_agents)
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                st.stop()

        done_pills = "".join(f'<span class="pill pill-done">✓ {MODULE_LABELS[k]}</span>' for k in enabled_agents)
        st.markdown(f"<div style='margin:6px 0 10px;'>{done_pills}</div>", unsafe_allow_html=True)

        st.session_state.analysis_results = results
        st.session_state.risk_result      = risk_result
        st.session_state.analysis_done    = True
        st.success("✅ Analysis complete — scroll down to view results.")
        st.rerun()

    elif run_clicked and not enabled_agents:
        st.warning("Please enable at least one module in the sidebar.")

# ─── Results ───────────────────────────────────────────────────
if st.session_state.analysis_done and st.session_state.analysis_results:
    st.divider()
    results = st.session_state.analysis_results
    risk    = st.session_state.risk_result  # dict | None

    # Risk dashboard
    if risk and isinstance(risk, dict) and risk.get("scores"):
        scores = risk["scores"]
        col_h, col_f = st.columns([1, 1], gap="large")

        with col_h:
            st.markdown('<div class="overline">Contract Health Score</div>', unsafe_allow_html=True)
            overall = int(scores.get("overall", 5))
            legal_s = int(scores.get("legal", 5))
            fin_s   = int(scores.get("financial", 5))
            comp_s  = int(scores.get("compliance", 5))
            ops_s   = int(scores.get("operational", 5))

            CIRC = 251.3
            offset = CIRC - (overall / 10) * CIRC
            rc = ring_color(overall)
            bc, rl = risk_badge(overall)
            doc_name = st.session_state.filename.replace(".pdf","").replace(".docx","").replace(".txt","")
            doc_name = (doc_name[:26]+"…") if len(doc_name)>26 else doc_name

            # Score bars: score is 1-10, width = score * 10 %
            st.markdown(f"""
            <div class="risk-card">
                <div class="ring-wrap">
                    <div class="ring-box">
                        <svg width="96" height="96" viewBox="0 0 96 96">
                            <circle cx="48" cy="48" r="40" fill="none" stroke="#f1f5f9" stroke-width="9"/>
                            <circle cx="48" cy="48" r="40" fill="none" stroke="{rc}" stroke-width="9"
                                stroke-dasharray="{CIRC:.1f}" stroke-dashoffset="{offset:.1f}" stroke-linecap="round"/>
                        </svg>
                        <div class="ring-lbl"><div class="ring-num">{overall}</div><div class="ring-den">/10</div></div>
                    </div>
                    <div>
                        <div style="font-size:10px;text-transform:uppercase;letter-spacing:1px;color:#94a3b8;font-weight:700;margin-bottom:3px;">Risk Score</div>
                        <div style="font-size:15px;font-weight:700;color:#0c1526;margin-bottom:5px;">{doc_name}</div>
                        <div style="font-size:11.5px;color:#64748b;margin-bottom:5px;">{st.session_state.contract_type}</div>
                        <div class="risk-badge {bc}">{rl}</div>
                    </div>
                </div>
                <div class="score-row"><div class="score-lbl">Legal</div>
                    <div class="bar-bg"><div class="bar-fill {bar_class(legal_s)}" style="width:{legal_s*10}%;"></div></div>
                    <div class="score-num">{legal_s}</div></div>
                <div class="score-row"><div class="score-lbl">Compliance</div>
                    <div class="bar-bg"><div class="bar-fill {bar_class(comp_s)}" style="width:{comp_s*10}%;"></div></div>
                    <div class="score-num">{comp_s}</div></div>
                <div class="score-row"><div class="score-lbl">Financial</div>
                    <div class="bar-bg"><div class="bar-fill {bar_class(fin_s)}" style="width:{fin_s*10}%;"></div></div>
                    <div class="score-num">{fin_s}</div></div>
                <div class="score-row" style="margin-bottom:0"><div class="score-lbl">Operational</div>
                    <div class="bar-bg"><div class="bar-fill {bar_class(ops_s)}" style="width:{ops_s*10}%;"></div></div>
                    <div class="score-num">{ops_s}</div></div>
            </div>
            """, unsafe_allow_html=True)

        with col_f:
            st.markdown('<div class="overline">Risk Factors & Protective Clauses</div>', unsafe_allow_html=True)
            def sev_badge(level):
                cls = {"critical":"b-critical","high":"b-high","medium":"b-medium","low":"b-low"}.get(level.lower(),"b-medium")
                return f'<span class="badge {cls}">{level.upper()}</span>'

            rf_list  = scores.get("risk_factors", [])
            pos_list = scores.get("positives", [])
            if rf_list:
                sevs = ["critical","high","high","medium","medium"]
                items = "".join(f'<div class="rf-item"><div style="padding-top:1px;min-width:66px;">{sev_badge(sevs[min(i,4)])}</div><div><div class="rf-title">{rf}</div></div></div>' for i,rf in enumerate(rf_list[:5]))
                st.markdown(f'<div class="risk-card" style="padding:18px 22px;">{items}</div>', unsafe_allow_html=True)
            if pos_list:
                pos_html = "".join(f'<li style="color:#065f46;font-size:13px;margin-bottom:5px;">✅ {p}</li>' for p in pos_list)
                st.markdown(f'<div class="risk-card" style="padding:18px 22px;margin-top:12px;"><div class="overline">Protective Clauses</div><ul style="margin:0;padding-left:18px;list-style:none;">{pos_html}</ul></div>', unsafe_allow_html=True)

        st.divider()

    # Export toolbar
    st.markdown("## Analysis Report")
    all_for_report = dict(results)
    if risk and isinstance(risk, dict) and risk.get("narrative"):
        all_for_report["risk"] = risk["narrative"]

    full_md  = build_full_report(all_for_report, st.session_state.filename)
    full_txt = build_plain_text_report(all_for_report, st.session_state.filename)

    dl1, dl2, re_col, _ = st.columns([1,1,1,3])
    with dl1: st.download_button("⬇ Download .md",  data=full_md.encode("utf-8"),  file_name=f"clauseai_{st.session_state.filename}.md",  mime="text/markdown")
    with dl2: st.download_button("⬇ Download .txt", data=full_txt.encode("utf-8"), file_name=f"clauseai_{st.session_state.filename}.txt", mime="text/plain")
    with re_col:
        if st.button("↺  Re-analyse"):
            for k in ["analysis_done","analysis_results","risk_result","chat_history","word_count"]:
                st.session_state[k] = _DEFAULTS.get(k)
            st.rerun()
    st.markdown("---")

    # Tabs
    tab_names = ["📋 All Sections"]
    if risk and isinstance(risk, dict): tab_names.append("🚨 Risk Summary")
    tab_names += ["📄 Executive Summary","⚖️ Legal","🛡️ Compliance","📈 Finance","⚙️ Operations"]
    if "simplifier" in results: tab_names.append("💬 Plain English")
    tabs = st.tabs(tab_names)
    t = 0

    def show(title, content, exp=True):
        with st.expander(title, expanded=exp):
            st.markdown(content if isinstance(content, str) else str(content))

    with tabs[t]:
        t += 1
        shown = False
        for key in ["summary","legal","compliance","finance","operations","simplifier"]:
            if key in results:
                show(SECTION_LABELS.get(key, key.title()), results[key], auto_expand); shown = True
        if risk and isinstance(risk, dict) and risk.get("narrative"):
            show("🚨 Risk Narrative", risk["narrative"], auto_expand); shown = True
        if not shown: st.info("No results. Enable modules and re-run.")

    if risk and isinstance(risk, dict):
        with tabs[t]: t += 1; st.markdown(risk.get("narrative") or "_Risk narrative unavailable._")

    with tabs[t]: t += 1; st.markdown(results.get("summary") or "_Executive Summary not enabled._")
    with tabs[t]: t += 1; st.markdown(results.get("legal")   or "_Legal Review not enabled._")
    with tabs[t]: t += 1; st.markdown(results.get("compliance") or "_Compliance not enabled._")
    with tabs[t]: t += 1; st.markdown(results.get("finance")    or "_Finance not enabled._")
    with tabs[t]: t += 1; st.markdown(results.get("operations") or "_Operations not enabled._")
    if "simplifier" in results:
        with tabs[t]: st.markdown(results["simplifier"])

    # Q&A Section
    st.divider()
    qa_col, side_col = st.columns([3, 1], gap="large")

    with qa_col:
        st.markdown("## Contract Assistant")
        st.markdown("Ask anything about the contract — penalties, exit clauses, IP, liability, obligations.")
        st.markdown("**Quick questions:**")
        QUICK_QS = [
            "What are the penalties for late payment?",
            "Can either party terminate early?",
            "Who owns the intellectual property?",
            "What are the liability limits?",
        ]
        q_cols = st.columns(4)
        for i, q in enumerate(QUICK_QS):
            if q_cols[i].button(q, key=f"qq_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":q})
                with st.spinner("Consulting the contract…"):
                    answer = ask_contract(q, st.session_state.contract_text, safe_ctx(results))
                st.session_state.chat_history.append({"role":"assistant","content":answer})
                st.rerun()

        # st.markdown("---")
        # for msg in st.session_state.chat_history:
        #     with st.chat_message(msg["role"], avatar="👤" if msg["role"]=="user" else "📋"):
        #         st.markdown(msg["content"])

        # if user_q := st.chat_input("Ask anything about this contract…"):
        #     st.session_state.chat_history.append({"role":"user","content":user_q})
        #     with st.chat_message("user", avatar="👤"): st.markdown(user_q)
        #     with st.chat_message("assistant", avatar="📋"):
        #         with st.spinner("Consulting the contract…"):
        #             answer = ask_contract(user_q, st.session_state.contract_text, safe_ctx(results))
        #         st.markdown(answer)
        #     st.session_state.chat_history.append({"role":"assistant","content":answer})
        st.markdown("---")

        # Scrollable chat area
        chat_container = st.container(height=400)

        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(
                    msg["role"],
                    avatar="👤" if msg["role"] == "user" else "📋"
                ):
                    st.markdown(msg["content"])

        # Input below the chat history
        user_q = st.chat_input("Ask anything about this contract…")

        if user_q:
            st.session_state.chat_history.append(
                {"role": "user", "content": user_q}
            )

            with st.spinner("Consulting the contract…"):
                answer = ask_contract(
                    user_q,
                    st.session_state.contract_text,
                    safe_ctx(results),
                )

            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )

        st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑  Clear Chat", key="clear_chat"):
                st.session_state.chat_history = []; st.rerun()

    with side_col:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="overline">Export</div>', unsafe_allow_html=True)
        st.download_button("⬇  Full Report (.md)", data=full_md.encode("utf-8"),
            file_name=f"clauseai_{st.session_state.filename}.md", mime="text/markdown", use_container_width=True)
        st.download_button("📄  Plain Text (.txt)", data=full_txt.encode("utf-8"),
            file_name=f"clauseai_{st.session_state.filename}.txt", mime="text/plain", use_container_width=True)

        if st.session_state.word_count:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="overline">Contract Info</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:14px 16px;"><div style="font-size:13px;font-weight:700;color:#0c1526;">{st.session_state.word_count:,} words</div><div style="font-size:12px;color:#64748b;margin-top:2px;">{st.session_state.contract_type}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="overline">Recent Contracts</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="recent-item"><span style="font-size:15px">📄</span>
            <div class="recent-info"><div class="recent-name">Vendor NDA — TechFlow</div><div class="recent-date">May 28</div></div>
            <span class="done-chip">Done</span></div>
        <div class="recent-item"><span style="font-size:15px">📄</span>
            <div class="recent-info"><div class="recent-name">SaaS Agreement — Orbit</div><div class="recent-date">May 20</div></div>
            <span class="done-chip">Done</span></div>
        <div class="recent-item"><span style="font-size:15px">📄</span>
            <div class="recent-info"><div class="recent-name">Employment Contract</div><div class="recent-date">May 12</div></div>
            <span class="done-chip">Done</span></div>
        """, unsafe_allow_html=True)

# ─── Empty State ───────────────────────────────────────────────
elif not uploaded_file:
    st.markdown("---")
    features = [
        ("⚖️","Legal Review","Risky clauses, liability gaps, ambiguous wording, and termination conditions."),
        ("📈","Financial Risk","Payment terms, hidden costs, penalties, financial exposure, and currency risk."),
        ("🛡️","Compliance Check","GDPR, data privacy, regulatory gaps, missing disclosures, and labour law."),
        ("⚙️","Operations Review","Delivery timelines, SLAs, responsibilities, exit & transition obligations."),
        ("🚨","Risk Scoring","Overall + domain risk scores (1–10), top risk factors, and protective clauses."),
        ("💬","Contract Assistant","Ask specific questions about the contract after analysis completes."),
    ]
    r1 = st.columns(3, gap="medium"); r2 = st.columns(3, gap="medium")
    for i,(icon,title,desc) in enumerate(features):
        with (r1[i] if i<3 else r2[i-3]):
            st.markdown(f'<div class="feat-card"><div class="feat-icon">{icon}</div><div class="feat-title">{title}</div><div class="feat-desc">{desc}</div></div>', unsafe_allow_html=True)