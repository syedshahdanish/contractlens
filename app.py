import streamlit as st
import plotly.graph_objects as go
from contract_analyzer import extract_pdf_text, analyze_contract, chat_with_contract

st.set_page_config(
    page_title="ContractLens",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════════════
#  DESIGN SYSTEM — Dark noir + amber accent
#  Typography: Fraunces (display) · Manrope (body) · JetBrains Mono (data)
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700;9..144,900&family=Manrope:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at top, rgba(245,158,11,0.05) 0%, transparent 50%),
        radial-gradient(ellipse at bottom right, rgba(239,68,68,0.03) 0%, transparent 50%),
        #09090F;
    font-family: 'Manrope', sans-serif;
    color: #F4F4F5;
}
.block-container { padding-top: 2.5rem; padding-bottom: 4rem; max-width: 1100px; }

/* Keep menu visible — header transparent only */
header[data-testid="stHeader"] { background: transparent !important; backdrop-filter: blur(8px); }
footer { visibility: hidden; }

/* ── Hero ─────────────────────────────────── */
.hero {
    margin-bottom: 3rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    animation: fadeUp 0.6s ease-out;
}
.hero-row { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1.2rem; }
.hero-logo {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #F59E0B 0%, #EAB308 100%);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Fraunces', serif; font-weight: 900; font-size: 1.2rem;
    color: #09090F;
}
.hero-brand { font-weight: 700; font-size: 1rem; color: #F4F4F5; letter-spacing: -0.01em; }
.hero-tag {
    font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
    color: #F59E0B; background: rgba(245,158,11,0.08);
    padding: 0.3rem 0.7rem; border-radius: 4px;
    border: 1px solid rgba(245,158,11,0.2); margin-left: auto;
}
.hero h1 {
    font-family: 'Fraunces', serif !important;
    font-weight: 700; font-size: 4.5rem; line-height: 1.0;
    letter-spacing: -0.04em; margin: 0;
    background: linear-gradient(180deg, #F4F4F5 0%, #71717A 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero .subtitle {
    font-size: 1.15rem; color: #A1A1AA;
    margin-top: 1rem; max-width: 600px; line-height: 1.5;
}

/* ── Section titles ────────────────────────── */
.section-h {
    font-family: 'Fraunces', serif; font-weight: 600;
    font-size: 1.8rem; color: #F4F4F5;
    margin: 3rem 0 1.5rem 0; letter-spacing: -0.02em;
}
.section-h::before {
    content: ''; display: inline-block;
    width: 6px; height: 6px; background: #F59E0B; border-radius: 50%;
    margin-right: 0.8rem; vertical-align: middle;
}

/* ── Animations ────────────────────────────── */
@keyframes fadeUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

/* ── Mono label ────────────────────────────── */
.label-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; font-weight: 500;
    text-transform: uppercase; letter-spacing: 0.2em;
    color: #71717A;
}

/* ── Glass card ────────────────────────────── */
.risk-glass-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.risk-glass-card:hover {
    border-color: rgba(245,158,11,0.2);
    transform: translateY(-2px);
}

/* ── Summary block ─────────────────────────── */
.summary-block {
    background: rgba(255,255,255,0.02);
    border-left: 2px solid #F59E0B;
    padding: 1.5rem 1.8rem;
    border-radius: 0 8px 8px 0;
    margin-top: 0.5rem;
}
.summary-block p {
    font-family: 'Fraunces', serif; font-size: 1.15rem;
    line-height: 1.65; color: #E5E5E8; margin: 0;
    font-style: italic; font-weight: 400;
}

/* ── Negotiation cards ─────────────────────── */
.nego-card {
    background: rgba(255,255,255,0.02);
    padding: 1.2rem 1.5rem;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid #F59E0B;
    transition: all 0.2s ease;
    margin-bottom: 0.7rem;
}
.nego-card:hover { background: rgba(245,158,11,0.04); border-left-color: #FBB040; }
.nego-title { font-weight: 600; color: #F4F4F5; margin-bottom: 0.4rem; font-size: 0.95rem; }
.nego-body { color: #A1A1AA; font-size: 0.92rem; line-height: 1.55; }

/* ── File uploader ─────────────────────────── */
.stFileUploader > section {
    background: rgba(255,255,255,0.02) !important;
    border: 2px dashed rgba(245,158,11,0.25) !important;
    border-radius: 12px !important;
    padding: 2rem !important;
    transition: all 0.2s ease;
}
.stFileUploader > section:hover {
    border-color: rgba(245,158,11,0.5) !important;
    background: rgba(245,158,11,0.03) !important;
}

/* ── Expanders ─────────────────────────────── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    margin-bottom: 0.6rem !important;
    transition: all 0.2s ease;
}
[data-testid="stExpander"]:hover {
    background: rgba(255,255,255,0.04) !important;
    border-color: rgba(245,158,11,0.15) !important;
}
[data-testid="stExpander"] summary p { color: #F4F4F5 !important; font-weight: 500 !important; }
[data-testid="stExpander"] em { color: #71717A !important; }

/* ── Chat ──────────────────────────────────── */
.stChatMessage {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
}

.stSpinner > div { border-top-color: #F59E0B !important; }

/* ── Responsive ────────────────────────────── */
@media (max-width: 768px) {
    .hero h1 { font-size: 2.5rem !important; }
    .block-container { padding: 1.5rem 1rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  HERO
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-row">
        <div class="hero-logo">C</div>
        <div class="hero-brand">ContractLens</div>
        <div class="hero-tag">AI · GEMINI 2.5</div>
    </div>
    <h1>See every risk<br>before you sign.</h1>
    <div class="subtitle">AI-powered contract analysis. Upload any agreement and get risk scores, plain-English explanations, and negotiation strategy in 30 seconds.</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  STATE
# ═══════════════════════════════════════════════════════════════
if "analysis" not in st.session_state:
    st.session_state.analysis = None
    st.session_state.contract_text = None
    st.session_state.chat_history = []

# ═══════════════════════════════════════════════════════════════
#  UPLOAD
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="label-mono" style="margin-bottom:0.8rem;">UPLOAD CONTRACT</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload contract PDF", type="pdf", label_visibility="collapsed")

if uploaded_file and st.session_state.analysis is None:
    with st.spinner("Reading the contract..."):
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())
        st.session_state.contract_text = extract_pdf_text("temp.pdf")
    with st.spinner("Analyzing with Gemini 2.5 Flash..."):
        st.session_state.analysis = analyze_contract(st.session_state.contract_text)

# ═══════════════════════════════════════════════════════════════
#  CHARTS
# ═══════════════════════════════════════════════════════════════
def render_gauge(score, level):
    color_map = {"High": "#EF4444", "Medium": "#F59E0B", "Low": "#10B981"}
    color = color_map.get(level, "#F59E0B")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'font': {'size': 56, 'family': 'Fraunces', 'color': '#F4F4F5'},
                'suffix': '<span style="font-size:22px;color:#52525B"> /10</span>'},
        gauge={
            'axis': {'range': [0, 10], 'tickwidth': 0,
                     'tickfont': {'color': '#71717A', 'size': 10, 'family': 'JetBrains Mono'}},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "rgba(255,255,255,0.02)",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 4], 'color': "rgba(16,185,129,0.08)"},
                {'range': [4, 7], 'color': "rgba(245,158,11,0.08)"},
                {'range': [7, 10], 'color': "rgba(239,68,68,0.08)"},
            ],
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(t=20, b=10, l=30, r=30), height=260)
    return fig

def render_donut(risks):
    counts = {"High": 0, "Medium": 0, "Low": 0}
    for r in risks:
        counts[r['severity']] = counts.get(r['severity'], 0) + 1
    fig = go.Figure(data=[go.Pie(
        labels=list(counts.keys()),
        values=list(counts.values()),
        hole=0.65,
        marker=dict(colors=['#EF4444', '#F59E0B', '#10B981'],
                    line=dict(color='#09090F', width=2)),
        textfont=dict(family='JetBrains Mono', size=12, color='#F4F4F5'),
        textinfo='value',
    )])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10, b=10, l=10, r=10), height=240,
        legend=dict(orientation='h', y=-0.1,
                    font=dict(family='Manrope', color='#A1A1AA', size=11)),
        annotations=[dict(
            text=f'<b style="color:#F4F4F5;font-family:Fraunces;font-size:26px">{sum(counts.values())}</b><br><span style="color:#71717A;font-family:monospace;font-size:9px;letter-spacing:2px">RISKS</span>',
            x=0.5, y=0.5, showarrow=False)]
    )
    return fig

# ═══════════════════════════════════════════════════════════════
#  RESULTS
# ═══════════════════════════════════════════════════════════════
if st.session_state.analysis:
    a = st.session_state.analysis

    # Row 1: Gauge + Summary
    c1, c2 = st.columns([1, 1.3], gap="large")
    with c1:
        st.markdown('<div class="label-mono" style="margin-top:1rem;">RISK ASSESSMENT</div>', unsafe_allow_html=True)
        st.plotly_chart(render_gauge(a['risk_score'], a['risk_level']),
                        use_container_width=True, config={'displayModeBar': False})
    with c2:
        st.markdown('<div class="label-mono" style="margin-top:1rem;">SUMMARY</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="summary-block"><p>{a["summary"]}</p></div>', unsafe_allow_html=True)

    # Row 2: Donut + Stats
    c3, c4 = st.columns([1, 1.3], gap="large")
    with c3:
        st.markdown('<div class="label-mono" style="margin-top:1rem;">RISK DISTRIBUTION</div>', unsafe_allow_html=True)
        st.plotly_chart(render_donut(a['risks']),
                        use_container_width=True, config={'displayModeBar': False})
    with c4:
        st.markdown('<div class="label-mono" style="margin-top:1rem;">KEY METRICS</div>', unsafe_allow_html=True)
        h = sum(1 for r in a['risks'] if r['severity'] == 'High')
        m = sum(1 for r in a['risks'] if r['severity'] == 'Medium')
        l = sum(1 for r in a['risks'] if r['severity'] == 'Low')
        t = len(a['negotiation_suggestions'])
        st.markdown(f"""
        <div class="risk-glass-card" style="margin-top:0.5rem;">
            <div style="display:flex;justify-content:space-between;text-align:left;">
                <div><div class="label-mono">HIGH</div>
                <div style="font-family:'Fraunces',serif;font-size:2.5rem;color:#EF4444;font-weight:700;line-height:1;">{h}</div></div>
                <div><div class="label-mono">MED</div>
                <div style="font-family:'Fraunces',serif;font-size:2.5rem;color:#F59E0B;font-weight:700;line-height:1;">{m}</div></div>
                <div><div class="label-mono">LOW</div>
                <div style="font-family:'Fraunces',serif;font-size:2.5rem;color:#10B981;font-weight:700;line-height:1;">{l}</div></div>
                <div><div class="label-mono">TIPS</div>
                <div style="font-family:'Fraunces',serif;font-size:2.5rem;color:#F4F4F5;font-weight:700;line-height:1;">{t}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Risks
    st.markdown('<div class="section-h">Identified Risks</div>', unsafe_allow_html=True)
    dots = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
    for risk in a['risks']:
        with st.expander(f"{dots.get(risk['severity'], '⚪')}  **{risk['title']}**   ·   {risk['severity']}"):
            st.write(risk['explanation'])
            st.markdown(f"*\"{risk['clause_excerpt']}\"*")

    # Negotiation
    st.markdown('<div class="section-h">Negotiation Strategy</div>', unsafe_allow_html=True)
    nego_html = ""
    for tip in a['negotiation_suggestions']:
        nego_html += f'<div class="nego-card"><div class="nego-title">{tip["issue"]}</div><div class="nego-body">{tip["suggestion"]}</div></div>'
    st.markdown(nego_html, unsafe_allow_html=True)

    # Chat
    st.markdown('<div class="section-h">Ask the Contract</div>', unsafe_allow_html=True)
    for q, ans in st.session_state.chat_history:
        with st.chat_message("user", avatar="👤"):
            st.write(q)
        with st.chat_message("assistant", avatar="⚖️"):
            st.write(ans)
    question = st.chat_input("Ask anything about the contract...")
    if question:
        with st.spinner("Thinking..."):
            answer, st.session_state.chat_history = chat_with_contract(
                st.session_state.contract_text, question, st.session_state.chat_history)
        st.rerun()
else:
    st.markdown("""
    <div style="margin-top:3rem;text-align:center;opacity:0.4;">
        <div class="label-mono">↑  UPLOAD A CONTRACT TO BEGIN</div>
    </div>
    """, unsafe_allow_html=True)