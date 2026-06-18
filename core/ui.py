"""
core/ui.py - All UI Components, Styling, and Layout
Single source of truth for every visual decision in the app.
"""

import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import math

# ============================================================================
# DESIGN TOKENS
# ============================================================================
# Palette
C_BG          = "#0F1117"   # page background
C_SURFACE     = "#1A1D27"   # card / panel background
C_SURFACE_2   = "#21263A"   # elevated surface
C_BORDER      = "#2A2F45"   # subtle border
C_PRIMARY     = "#6366F1"   # indigo accent
C_PRIMARY_DIM = "#4F46E5"   # darker indigo
C_SUCCESS     = "#10B981"   # emerald
C_WARNING     = "#F59E0B"   # amber
C_DANGER      = "#F43F5E"   # rose
C_TEXT        = "#F1F5F9"   # primary text
C_TEXT_MUTED  = "#64748B"   # secondary text
C_BIT_0       = "#38BDF8"   # sky blue  — zero bit
C_BIT_1       = "#FBBF24"   # amber     — one  bit

# ============================================================================
# GLOBAL CSS
# ============================================================================

def apply_custom_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        /* ── Reset & base ─────────────────────────────────── */
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            background-color: {C_BG};
            color: {C_TEXT};
        }}
        .main .block-container {{
            padding: 1.5rem 2.5rem 3rem 2.5rem;
            max-width: 1100px;
        }}
        /* Kill Streamlit's default white background on widgets */
        .stTextArea textarea,
        .stSlider,
        div[data-baseweb="input"] input {{
            background: {C_SURFACE_2} !important;
            color: {C_TEXT} !important;
            border-color: {C_BORDER} !important;
        }}
        .stTextArea textarea:focus {{
            border-color: {C_PRIMARY} !important;
            box-shadow: 0 0 0 2px {C_PRIMARY}33 !important;
        }}
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: {C_SURFACE};
            border-right: 1px solid {C_BORDER};
        }}
        [data-testid="stSidebar"] * {{
            color: {C_TEXT} !important;
        }}
        [data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
        [data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] {{
            color: {C_TEXT_MUTED} !important;
        }}
        /* Remove stray white block above sidebar widgets */
        [data-testid="stSidebar"] .element-container {{
            background: transparent;
        }}
        /* Slider track */
        [data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] {{
            background-color: {C_PRIMARY} !important;
        }}
        [data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stThumbValue"] {{
            background-color: {C_PRIMARY} !important;
        }}
        /* Checkbox */
        [data-testid="stCheckbox"] label span {{
            color: {C_TEXT} !important;
        }}
        /* Plotly / chart backgrounds */
        .js-plotly-plot .plotly, .js-plotly-plot .plotly .svg-container {{
            background: {C_SURFACE} !important;
        }}
        /* Caption / small text */
        .stCaption, small {{
            color: {C_TEXT_MUTED} !important;
        }}
        /* Expander */
        .streamlit-expanderHeader {{
            background: {C_SURFACE_2} !important;
            color: {C_TEXT} !important;
            border-radius: 0.5rem;
            border: 1px solid {C_BORDER};
        }}
        .streamlit-expanderContent {{
            background: {C_SURFACE} !important;
            border: 1px solid {C_BORDER};
            border-top: none;
        }}
        /* Spinner text */
        [data-testid="stSpinner"] p {{ color: {C_TEXT_MUTED} !important; }}

        /* ── App header ───────────────────────────────────── */
        .app-header {{
            text-align: center;
            padding: 2rem 0 1rem 0;
        }}
        .app-title {{
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: {C_TEXT};
            margin: 0;
        }}
        .app-title span {{
            background: linear-gradient(135deg, {C_PRIMARY} 0%, #a78bfa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .app-subtitle {{
            color: {C_TEXT_MUTED};
            font-size: 0.95rem;
            margin-top: 0.4rem;
            font-weight: 400;
        }}

        /* ── Pipeline progress rail ───────────────────────── */
        .pipeline-rail {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
            margin: 1.5rem 0 2rem 0;
            overflow-x: auto;
            padding: 0.5rem 0;
        }}
        .pipeline-step {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.35rem;
            min-width: 90px;
        }}
        .pipeline-dot {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: {C_SURFACE_2};
            border: 2px solid {C_BORDER};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            font-weight: 700;
            color: {C_TEXT_MUTED};
            transition: all 0.2s;
            position: relative;
            z-index: 1;
        }}
        .pipeline-dot.active {{
            background: {C_PRIMARY};
            border-color: {C_PRIMARY};
            color: white;
            box-shadow: 0 0 0 4px {C_PRIMARY}33;
        }}
        .pipeline-label {{
            font-size: 0.7rem;
            font-weight: 600;
            color: {C_TEXT_MUTED};
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            white-space: nowrap;
        }}
        .pipeline-connector {{
            height: 2px;
            width: 40px;
            background: {C_BORDER};
            margin-bottom: 22px;
            flex-shrink: 0;
        }}

        /* ── Section header ───────────────────────────────── */
        .section-block {{
            background: {C_SURFACE};
            border: 1px solid {C_BORDER};
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            margin: 1.25rem 0 0.75rem 0;
        }}
        .section-title {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 1rem;
            font-weight: 700;
            color: {C_TEXT};
            margin: 0 0 0.1rem 0;
        }}
        .section-title .step-pill {{
            background: {C_PRIMARY}22;
            color: {C_PRIMARY};
            border: 1px solid {C_PRIMARY}44;
            border-radius: 20px;
            padding: 0.1rem 0.65rem;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}
        .section-desc {{
            font-size: 0.8rem;
            color: {C_TEXT_MUTED};
            margin: 0;
            font-weight: 400;
        }}

        /* ── Metric cards ─────────────────────────────────── */
        .metrics-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 0.75rem;
            margin: 0.75rem 0;
        }}
        .mcard {{
            background: {C_SURFACE_2};
            border: 1px solid {C_BORDER};
            border-radius: 10px;
            padding: 1rem 1.1rem;
            text-align: center;
        }}
        .mcard-val {{
            font-size: 1.6rem;
            font-weight: 800;
            line-height: 1.1;
            color: {C_TEXT};
        }}
        .mcard-val.primary  {{ color: {C_PRIMARY}; }}
        .mcard-val.success  {{ color: {C_SUCCESS}; }}
        .mcard-val.warning  {{ color: {C_WARNING}; }}
        .mcard-val.danger   {{ color: {C_DANGER};  }}
        .mcard-val.mono {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.1rem;
        }}
        .mcard-label {{
            font-size: 0.68rem;
            font-weight: 600;
            color: {C_TEXT_MUTED};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 0.3rem;
        }}
        .mcard-sub {{
            font-size: 0.78rem;
            color: {C_TEXT_MUTED};
            margin-top: 0.15rem;
        }}

        /* ── Bitstream display ────────────────────────────── */
        .bits-wrap {{
            margin: 0.6rem 0;
        }}
        .bits-label {{
            font-size: 0.7rem;
            font-weight: 600;
            color: {C_TEXT_MUTED};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.4rem;
        }}
        .bits-box {{
            background: #0D1016;
            border: 1px solid {C_BORDER};
            border-radius: 8px;
            padding: 0.9rem 1.1rem;
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            font-size: 0.88rem;
            line-height: 1.9;
            letter-spacing: 0.6px;
            word-break: break-all;
            white-space: pre-wrap;
            overflow-x: auto;
        }}
        .b0 {{ color: {C_BIT_0}; }}
        .b1 {{ color: {C_BIT_1}; }}
        .b-flip {{
            background: {C_DANGER}33;
            border-radius: 3px;
            outline: 1px solid {C_DANGER}66;
        }}
        .b-err {{
            background: {C_WARNING}22;
            border-radius: 3px;
            outline: 1px solid {C_WARNING}55;
        }}

        /* ── Info / status boxes ──────────────────────────── */
        .info-strip {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
            padding: 0.6rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            margin: 0.5rem 0;
        }}
        .info-strip.info    {{ background: {C_PRIMARY}18; border: 1px solid {C_PRIMARY}33; color: #a5b4fc; }}
        .info-strip.success {{ background: {C_SUCCESS}18; border: 1px solid {C_SUCCESS}33; color: #6ee7b7; }}
        .info-strip.warning {{ background: {C_WARNING}18; border: 1px solid {C_WARNING}33; color: #fcd34d; }}
        .info-strip.danger  {{ background: {C_DANGER}18;  border: 1px solid {C_DANGER}33;  color: #fca5a5; }}

        /* ── Bit legend ───────────────────────────────────── */
        .bit-legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.2rem;
            margin: 0.4rem 0;
            font-size: 0.78rem;
            color: {C_TEXT_MUTED};
        }}
        .bit-legend span {{
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}
        .swatch {{
            width: 10px;
            height: 10px;
            border-radius: 2px;
            display: inline-block;
        }}

        /* ── Sidebar internals ────────────────────────────── */
        .sidebar-label {{
            font-size: 0.72rem;
            font-weight: 700;
            color: {C_TEXT_MUTED};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.3rem;
        }}
        .sidebar-chip {{
            background: {C_SURFACE_2};
            border: 1px solid {C_BORDER};
            border-radius: 8px;
            padding: 0.6rem 0.9rem;
            font-size: 0.82rem;
            color: {C_TEXT_MUTED};
            text-align: center;
            margin-top: 0.5rem;
            line-height: 1.6;
        }}
        .sidebar-chip strong {{ color: {C_PRIMARY}; }}
        .sidebar-divider {{
            border: none;
            border-top: 1px solid {C_BORDER};
            margin: 1rem 0;
        }}

        /* ── Responsive ───────────────────────────────────── */
        @media (max-width: 640px) {{
            .app-title {{ font-size: 1.6rem; }}
            .main .block-container {{ padding: 1rem; }}
            .metrics-row {{ grid-template-columns: 1fr 1fr; }}
            .bits-box {{ font-size: 0.72rem; padding: 0.6rem; }}
            .pipeline-connector {{ width: 20px; }}
        }}
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# LAYOUT COMPONENTS
# ============================================================================

def render_header():
    st.markdown("""
    <div class="app-header">
        <h1 class="app-title">⟨ <span>Conv. Encoder</span> &amp; Viterbi Decoder ⟩</h1>
        <p class="app-subtitle">Step-by-step forward error correction — encode, transmit through noise, decode</p>
    </div>
    """, unsafe_allow_html=True)


def render_pipeline_rail(active_step=None):
    """
    Render the 5-step pipeline progress rail.
    active_step: int 1–5, or None for all inactive (just decorative).
    """
    steps = [
        ("1", "Text → Bits"),
        ("2", "Encode"),
        ("3", "Channel"),
        ("4", "Decode"),
        ("5", "Results"),
    ]
    html = '<div class="pipeline-rail">'
    for i, (num, label) in enumerate(steps):
        is_active = (active_step is not None and int(num) <= active_step)
        dot_class = "pipeline-dot active" if is_active else "pipeline-dot"
        html += f"""
        <div class="pipeline-step">
            <div class="{dot_class}">{num}</div>
            <div class="pipeline-label">{label}</div>
        </div>
        """
        if i < len(steps) - 1:
            html += '<div class="pipeline-connector"></div>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_section(step_num, title, description=""):
    """Render a section block header."""
    desc_html = f'<p class="section-desc">{description}</p>' if description else ""
    st.markdown(f"""
    <div class="section-block">
        <div class="section-title">
            <span class="step-pill">Step {step_num}</span>
            {title}
        </div>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("## Pipeline Controls")
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

        st.markdown('<div class="sidebar-label">Input Message</div>', unsafe_allow_html=True)
        input_text = st.text_area(
            "message",
            value="Hello World",
            max_chars=200,
            help="Any text — converted to 8-bit ASCII",
            label_visibility="collapsed"
        )

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">Channel SNR</div>', unsafe_allow_html=True)
        snr_db = st.slider(
            "Signal-to-Noise Ratio (dB)",
            min_value=0.0, max_value=15.0,
            value=5.0, step=0.5,
            help="Higher = less noise = better recovery",
            label_visibility="collapsed"
        )

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">Display Options</div>', unsafe_allow_html=True)
        show_trellis  = st.checkbox("Trellis Diagram",   value=True)
        show_ber_plot = st.checkbox("BER Analysis Plot", value=True)

        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        st.markdown("""
        <div class="sidebar-chip">
            <strong>Rate 1/2 · K = 3</strong><br>
            G₁ = 111 &nbsp;·&nbsp; G₂ = 101
        </div>
        """, unsafe_allow_html=True)

    return input_text, snr_db, show_trellis, show_ber_plot


# ============================================================================
# BIT DISPLAY
# ============================================================================

def render_bits(bits, label="Bitstream", flipped=None, errors=None):
    """
    bits:    binary string
    label:   label shown above
    flipped: list of indices flipped by channel noise  → red outline
    errors:  list of indices that are wrong after decode → amber outline
    """
    if flipped is None: flipped = []
    if errors  is None: errors  = []

    html = ""
    for i, b in enumerate(bits):
        cls = "b1" if b == "1" else "b0"
        extra = ""
        if i in flipped: extra = " b-flip"
        elif i in errors: extra = " b-err"
        html += f'<span class="{cls}{extra}">{b}</span>'

    st.markdown(f"""
    <div class="bits-wrap">
        <div class="bits-label">{label}</div>
        <div class="bits-box">{html}</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"📏 {len(bits)} bits")


def render_bit_legend(show_flipped=False, show_errors=False):
    parts = [
        f'<span><span class="swatch" style="background:{C_BIT_0}"></span>Bit 0</span>',
        f'<span><span class="swatch" style="background:{C_BIT_1}"></span>Bit 1</span>',
    ]
    if show_flipped:
        parts.append(f'<span><span class="swatch" style="background:{C_DANGER}55;outline:1px solid {C_DANGER}88"></span>Flipped by noise</span>')
    if show_errors:
        parts.append(f'<span><span class="swatch" style="background:{C_WARNING}33;outline:1px solid {C_WARNING}66"></span>Decoding error</span>')
    st.markdown(f'<div class="bit-legend">{"".join(parts)}</div>', unsafe_allow_html=True)


# ============================================================================
# METRIC CARDS
# ============================================================================

def render_metrics(metrics):
    """
    metrics: list of dicts
        value       – display value (str)
        label       – small label below
        color_class – one of: primary | success | warning | danger | (blank = default)
        sub         – optional tiny sub-label
        mono        – if True, apply monospace class to value
    """
    html = '<div class="metrics-row">'
    for m in metrics:
        val_cls = "mcard-val"
        if m.get("color_class"): val_cls += f" {m['color_class']}"
        if m.get("mono"):        val_cls += " mono"
        sub = f'<div class="mcard-sub">{m["sub"]}</div>' if m.get("sub") else ""
        html += f"""
        <div class="mcard">
            <div class="{val_cls}">{m['value']}</div>
            <div class="mcard-label">{m['label']}</div>
            {sub}
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ============================================================================
# INFO STRIP
# ============================================================================

def render_info(message, kind="info"):
    """kind: info | success | warning | danger"""
    icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "danger": "🚫"}
    st.markdown(f"""
    <div class="info-strip {kind}">
        <span>{icons.get(kind, "ℹ️")}</span>
        <span>{message}</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# TRELLIS DIAGRAM
# ============================================================================

def render_trellis(trellis_path, state_labels=('00', '01', '10', '11')):
    if not trellis_path:
        render_info("No trellis path available.", "warning")
        return

    num_steps = len(trellis_path) + 1

    fig = go.Figure()

    # ── Background grid nodes (all states, all steps) ──────────────────
    node_x, node_y, node_text = [], [], []
    for step in range(num_steps):
        for s in range(4):
            node_x.append(step)
            node_y.append(s)
            node_text.append(f"t={step} | state {state_labels[s]}")

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode="markers",
        marker=dict(size=10, color=C_BORDER, line=dict(width=1, color=C_SURFACE_2)),
        showlegend=False,
        hoverinfo="text",
        text=node_text
    ))

    # ── Winning path ───────────────────────────────────────────────────
    px, py, ph = [], [], []
    for i, t in enumerate(trellis_path):
        fs, ts_, ib = t["from_state"], t["to_state"], t["input_bit"]
        px.extend([i, i + 1, None])
        py.extend([fs, ts_, None])
        ph.extend([f"t={i}→{i+1} | {fs}→{ts_} | in={ib}", "", ""])

        mid_x = i + 0.5
        mid_y = (fs + ts_) / 2
        fig.add_annotation(
            x=mid_x, y=mid_y + 0.25,
            text=str(ib),
            showarrow=False,
            font=dict(size=10, color=C_PRIMARY, family="JetBrains Mono"),
            bgcolor=C_SURFACE,
            bordercolor=C_BORDER,
            borderwidth=1,
            borderpad=2,
        )

    fig.add_trace(go.Scatter(
        x=px, y=py,
        mode="lines+markers",
        line=dict(color=C_PRIMARY, width=3),
        marker=dict(size=12, color=C_PRIMARY, symbol="diamond",
                    line=dict(width=2, color="white")),
        name="ML Path",
        hoverinfo="text",
        text=ph,
        connectgaps=False
    ))

    fig.update_layout(
        paper_bgcolor=C_SURFACE,
        plot_bgcolor="#0D1016",
        font=dict(family="Inter", color=C_TEXT, size=12),
        title=dict(
            text="Maximum-Likelihood Trellis Path",
            font=dict(size=14, color=C_TEXT),
            x=0.5
        ),
        xaxis=dict(
            title="Time Step",
            color=C_TEXT_MUTED,
            gridcolor=C_BORDER,
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            title="State",
            tickmode="array",
            tickvals=[0, 1, 2, 3],
            ticktext=list(state_labels),
            color=C_TEXT_MUTED,
            gridcolor=C_BORDER,
            showgrid=True,
            zeroline=False,
        ),
        height=380,
        margin=dict(l=50, r=30, t=50, b=50),
        showlegend=True,
        legend=dict(
            bgcolor=C_SURFACE_2,
            bordercolor=C_BORDER,
            borderwidth=1,
            font=dict(color=C_TEXT),
        ),
        hovermode="closest",
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================================
# BER PLOT
# ============================================================================

def render_ber_plot(snr_values, ber_values, theoretical_ber=None):
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor(C_SURFACE)
    ax.set_facecolor("#0D1016")

    # Simulated
    ax.semilogy(snr_values, ber_values,
                "o-", label="Simulated (Viterbi)",
                color=C_PRIMARY, markersize=6, linewidth=2, zorder=3)

    # Theoretical
    if theoretical_ber:
        ax.semilogy(snr_values, theoretical_ber,
                    "--", label="Uncoded BPSK",
                    color=C_DANGER, linewidth=1.8, zorder=2)

    # Coding gain annotation
    if ber_values and min(ber_values) < 1e-3:
        for i, ber in enumerate(ber_values):
            if ber < 1e-3:
                ax.axhline(y=1e-3, color=C_TEXT_MUTED, linestyle=":", linewidth=1, alpha=0.6)
                ax.axvline(x=snr_values[i], color=C_TEXT_MUTED, linestyle=":", linewidth=1, alpha=0.6)
                gain = snr_values[i] - 6.5
                ax.text(snr_values[i] + 0.3, 2e-3, f"  Coding gain ≈ {gain:.1f} dB",
                        color=C_SUCCESS, fontsize=9,
                        bbox=dict(facecolor=C_SURFACE, edgecolor=C_BORDER,
                                  boxstyle="round,pad=0.3"))
                break

    for spine in ax.spines.values():
        spine.set_edgecolor(C_BORDER)
    ax.tick_params(colors=C_TEXT_MUTED, labelsize=10)
    ax.xaxis.label.set_color(C_TEXT_MUTED)
    ax.yaxis.label.set_color(C_TEXT_MUTED)
    ax.set_xlabel("SNR (dB)", fontsize=11)
    ax.set_ylabel("Bit Error Rate (BER)", fontsize=11)
    ax.set_title("BER vs SNR", fontsize=13, color=C_TEXT, pad=12)
    ax.grid(True, alpha=0.15, color=C_BORDER, linestyle="--")
    ax.set_ylim([1e-6, 1])
    legend = ax.legend(fontsize=10, loc="lower left",
                       facecolor=C_SURFACE_2, edgecolor=C_BORDER,
                       labelcolor=C_TEXT)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def render_ber_table(snr_values, ber_values, theoretical_ber=None):
    data = {"SNR (dB)": snr_values,
            "BER (Simulated)": [f"{b:.2e}" for b in ber_values]}
    if theoretical_ber:
        data["BER (Theoretical)"] = [f"{b:.2e}" for b in theoretical_ber]
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
