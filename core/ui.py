"""
core/ui.py - Premium Dashboard UI Components
Inspired by modern SaaS dashboards with dark theme, glass-morphism, and vibrant accents
"""

import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

# ============================================================================
# PREMIUM CSS - Complete Dashboard Styling
# ============================================================================

def apply_custom_css():
    """Apply premium modern dashboard CSS with dark theme and glass-morphism."""
    st.markdown("""
    <style>
        /* ===== IMPORTS & BASE ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            box-sizing: border-box;
        }
        
        /* ===== GLOBAL BACKGROUND ===== */
        .stApp {
            background: linear-gradient(160deg, #08081a 0%, #0f0f2a 30%, #1a1040 60%, #0a0a1f 100%);
            min-height: 100vh;
        }
        
        /* ===== MAIN CONTAINER ===== */
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }
        
        /* ===== SIDEBAR - Premium Dark ===== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d0d24 0%, #070716 100%) !important;
            border-right: 1px solid rgba(108, 99, 255, 0.08) !important;
            padding: 1.5rem 0.75rem !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stSlider,
        [data-testid="stSidebar"] .stTextArea {
            background: rgba(255, 255, 255, 0.02) !important;
            border-radius: 0.75rem !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
        }
        
        [data-testid="stSidebar"] .stTextArea textarea {
            background: rgba(255, 255, 255, 0.02) !important;
            color: rgba(255, 255, 255, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 0.75rem !important;
        }
        
        /* ===== SIDEBAR COMPONENTS ===== */
        .sidebar-brand {
            text-align: center;
            padding: 0.5rem 0 1.5rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            margin-bottom: 1.5rem;
        }
        
        .sidebar-brand-icon {
            font-size: 2.5rem;
            margin-bottom: 0.25rem;
        }
        
        .sidebar-brand-title {
            font-size: 1.3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6C63FF, #00D4FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        
        .sidebar-brand-sub {
            font-size: 0.65rem;
            color: rgba(255, 255, 255, 0.2);
            letter-spacing: 1px;
            text-transform: uppercase;
            font-weight: 500;
        }
        
        .sidebar-label {
            color: rgba(255, 255, 255, 0.3);
            font-size: 0.6rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            margin: 0.75rem 0 0.5rem 0;
            display: block;
        }
        
        .sidebar-divider {
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            margin: 1rem 0;
        }
        
        .sidebar-footer {
            color: rgba(255, 255, 255, 0.08);
            font-size: 0.65rem;
            text-align: center;
            margin-top: 1.5rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.03);
            line-height: 1.6;
        }
        
        .sidebar-footer strong {
            color: rgba(255, 255, 255, 0.15);
        }
        
        /* ===== MAIN HEADER ===== */
        .main-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 0 0.5rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
            gap: 0.75rem;
        }
        
        .main-title-group {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .main-title-icon {
            font-size: 2.2rem;
        }
        
        .main-title-text {
            font-size: 2rem;
            font-weight: 900;
            background: linear-gradient(135deg, #6C63FF 0%, #00D4FF 50%, #6C63FF 100%);
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
            animation: shimmer 4s ease-in-out infinite;
        }
        
        @keyframes shimmer {
            0%, 100% { background-position: 0% center; }
            50% { background-position: 200% center; }
        }
        
        .main-subtitle {
            font-size: 0.85rem;
            color: rgba(255, 255, 255, 0.25);
            font-weight: 400;
            letter-spacing: 0.2px;
        }
        
        .main-status-badge {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(0, 212, 255, 0.06);
            padding: 0.4rem 1rem;
            border-radius: 2rem;
            border: 1px solid rgba(0, 212, 255, 0.06);
        }
        
        .main-status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #00D4FF;
            animation: pulse-dot 2s ease-in-out infinite;
        }
        
        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(0.8); }
        }
        
        .main-status-text {
            font-size: 0.7rem;
            color: rgba(255, 255, 255, 0.3);
            font-weight: 500;
        }
        
        /* ===== SECTION CARDS ===== */
        .section-card {
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 1.25rem;
            border: 1px solid rgba(255, 255, 255, 0.04);
            padding: 1.5rem 1.75rem;
            margin: 1.25rem 0;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.2);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .section-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #6C63FF, #00D4FF, #6C63FF);
            background-size: 200% auto;
            opacity: 0;
            transition: opacity 0.4s ease;
            animation: shimmer-border 3s ease-in-out infinite;
        }
        
        @keyframes shimmer-border {
            0%, 100% { background-position: 0% center; }
            50% { background-position: 200% center; }
        }
        
        .section-card:hover {
            border-color: rgba(108, 99, 255, 0.12);
            box-shadow: 0 12px 60px rgba(108, 99, 255, 0.04);
            transform: translateY(-2px);
        }
        
        .section-card:hover::before {
            opacity: 1;
        }
        
        /* ===== SECTION HEADER ===== */
        .section-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
        }
        
        .section-number {
            background: linear-gradient(135deg, #6C63FF, #00D4FF);
            color: white;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: 800;
            box-shadow: 0 4px 20px rgba(108, 99, 255, 0.2);
            flex-shrink: 0;
        }
        
        .section-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.3px;
        }
        
        .section-badge {
            margin-left: auto;
            font-size: 0.6rem;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.15);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            background: rgba(255, 255, 255, 0.03);
            padding: 0.2rem 0.8rem;
            border-radius: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.04);
        }
        
        /* ===== BIT DISPLAY ===== */
        .bit-wrapper {
            background: rgba(0, 0, 0, 0.35);
            border-radius: 1rem;
            padding: 1rem 1.25rem;
            border: 1px solid rgba(255, 255, 255, 0.04);
            margin: 0.5rem 0;
            position: relative;
        }
        
        .bit-label {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: rgba(255, 255, 255, 0.25);
            font-size: 0.6rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }
        
        .bit-label .dot {
            width: 4px;
            height: 4px;
            border-radius: 50%;
            display: inline-block;
        }
        
        .bit-content {
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            font-size: 1rem;
            line-height: 2;
            letter-spacing: 0.5px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .bit-0 { color: #4FC3F7; }
        .bit-1 { color: #FFD54F; }
        
        .bit-error {
            background: rgba(255, 107, 107, 0.2);
            border-radius: 4px;
            padding: 0 3px;
            border-bottom: 2px solid #FF6B6B;
            animation: error-pulse 1.8s ease-in-out infinite;
        }
        
        .bit-flipped {
            background: rgba(255, 107, 107, 0.3);
            border-radius: 4px;
            padding: 0 3px;
            border-bottom: 2px solid #FF6B6B;
            animation: flip-pulse 1.2s ease-in-out infinite;
        }
        
        @keyframes error-pulse {
            0%, 100% { background: rgba(255, 107, 107, 0.1); }
            50% { background: rgba(255, 107, 107, 0.25); }
        }
        
        @keyframes flip-pulse {
            0%, 100% { background: rgba(255, 107, 107, 0.2); }
            50% { background: rgba(255, 107, 107, 0.45); }
        }
        
        .bit-length {
            color: rgba(255, 255, 255, 0.12);
            font-size: 0.65rem;
            text-align: right;
            margin-top: 0.3rem;
            font-weight: 500;
            letter-spacing: 0.5px;
        }
        
        /* ===== METRIC CARDS ===== */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 0.6rem;
            margin: 0.5rem 0 0.75rem 0;
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 0.75rem;
            padding: 0.75rem 1rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.03);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(108, 99, 255, 0.08);
            transform: translateY(-2px);
        }
        
        .metric-value {
            font-size: 1.4rem;
            font-weight: 800;
            line-height: 1.2;
            letter-spacing: -0.3px;
        }
        
        .metric-value.primary { 
            background: linear-gradient(135deg, #6C63FF, #00D4FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .metric-value.success { color: #00D4FF; }
        .metric-value.warning { color: #FFD54F; }
        .metric-value.danger { color: #FF6B6B; }
        .metric-value.white { color: rgba(255, 255, 255, 0.9); }
        .metric-value.gold { 
            background: linear-gradient(135deg, #FFD54F, #FF9A56);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .metric-label {
            font-size: 0.55rem;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.25);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-top: 0.15rem;
        }
        
        .metric-sub {
            font-size: 0.6rem;
            color: rgba(255, 255, 255, 0.1);
            margin-top: 0.05rem;
        }
        
        /* ===== STATUS INDICATOR ===== */
        .status-container {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.75rem 1.25rem;
            border-radius: 0.75rem;
            margin: 0.5rem 0;
        }
        
        .status-container.success {
            background: rgba(0, 212, 255, 0.06);
            border: 1px solid rgba(0, 212, 255, 0.08);
        }
        
        .status-container.warning {
            background: rgba(255, 213, 79, 0.06);
            border: 1px solid rgba(255, 213, 79, 0.08);
        }
        
        .status-container.danger {
            background: rgba(255, 107, 107, 0.06);
            border: 1px solid rgba(255, 107, 107, 0.08);
        }
        
        .status-icon {
            font-size: 1.8rem;
        }
        
        .status-text {
            flex: 1;
        }
        
        .status-title {
            font-weight: 700;
            font-size: 1rem;
        }
        
        .status-title.success { color: #00D4FF; }
        .status-title.warning { color: #FFD54F; }
        .status-title.danger { color: #FF6B6B; }
        
        .status-sub {
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.2);
        }
        
        .status-metric {
            font-weight: 700;
            font-size: 0.9rem;
        }
        
        .status-metric.success { color: #00D4FF; }
        .status-metric.warning { color: #FFD54F; }
        .status-metric.danger { color: #FF6B6B; }
        
        /* ===== LEGEND ===== */
        .legend-container {
            display: flex;
            gap: 1.25rem;
            flex-wrap: wrap;
            padding: 0.6rem 1rem;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 0.75rem;
            border: 1px solid rgba(255, 255, 255, 0.03);
            margin: 0.5rem 0;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.7rem;
            color: rgba(255, 255, 255, 0.3);
        }
        
        .legend-swatch {
            width: 14px;
            height: 14px;
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        
        /* ===== BADGE ===== */
        .badge {
            display: inline-block;
            padding: 0.2rem 1rem;
            border-radius: 2rem;
            font-weight: 700;
            font-size: 0.7rem;
            letter-spacing: 0.3px;
        }
        
        .badge-success {
            background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(0,212,255,0.05));
            color: #00D4FF;
            border: 1px solid rgba(0,212,255,0.1);
        }
        
        .badge-warning {
            background: linear-gradient(135deg, rgba(255,213,79,0.15), rgba(255,213,79,0.05));
            color: #FFD54F;
            border: 1px solid rgba(255,213,79,0.1);
        }
        
        .badge-danger {
            background: linear-gradient(135deg, rgba(255,107,107,0.15), rgba(255,107,107,0.05));
            color: #FF6B6B;
            border: 1px solid rgba(255,107,107,0.1);
        }
        
        .badge-info {
            background: linear-gradient(135deg, rgba(108,99,255,0.15), rgba(108,99,255,0.05));
            color: #6C63FF;
            border: 1px solid rgba(108,99,255,0.1);
        }
        
        /* ===== INFO BOX ===== */
        .info-box {
            padding: 0.6rem 1rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            font-weight: 500;
            font-size: 0.85rem;
            border-left: 3px solid;
        }
        
        .info-box.success {
            background: rgba(0, 212, 255, 0.04);
            border-color: #00D4FF;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .info-box.warning {
            background: rgba(255, 213, 79, 0.04);
            border-color: #FFD54F;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .info-box.danger {
            background: rgba(255, 107, 107, 0.04);
            border-color: #FF6B6B;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .info-box.info {
            background: rgba(108, 99, 255, 0.04);
            border-color: #6C63FF;
            color: rgba(255, 255, 255, 0.7);
        }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .main-title-text { font-size: 1.4rem; }
            .main-title-icon { font-size: 1.6rem; }
            .section-card { padding: 1rem; }
            .metric-grid { grid-template-columns: 1fr 1fr; }
            .bit-content { font-size: 0.7rem; }
            .main-header { flex-direction: column; align-items: flex-start; }
        }
        
        @media (max-width: 480px) {
            .metric-grid { grid-template-columns: 1fr; }
            .legend-container { flex-direction: column; gap: 0.3rem; }
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# COMPONENT FUNCTIONS
# ============================================================================

def render_sidebar():
    """Render premium sidebar with brand identity."""
    with st.sidebar:
        # Brand
        st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🔐</div>
            <div class="sidebar-brand-title">ConvEncoder</div>
            <div class="sidebar-brand-sub">Viterbi Decoder</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Message Input
        st.markdown('<span class="sidebar-label">📝 Message</span>', unsafe_allow_html=True)
        input_text = st.text_area(
            "",
            value="Hello World",
            max_chars=200,
            help="Type any text message to encode and transmit",
            label_visibility="collapsed",
            key="input_text"
        )
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # SNR Slider
        st.markdown('<span class="sidebar-label">📡 Signal-to-Noise Ratio</span>', unsafe_allow_html=True)
        snr_db = st.slider(
            "",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.5,
            help="Higher SNR = less noise = better recovery",
            label_visibility="collapsed",
            key="snr_slider"
        )
        
        # SNR visual indicator
        snr_percent = min(snr_db / 15.0 * 100, 100)
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.6rem; margin-top:0.2rem;">
            <div style="flex:1; height:3px; background:rgba(255,255,255,0.04); border-radius:4px; overflow:hidden;">
                <div style="width:{snr_percent}%; height:100%; background:linear-gradient(90deg, #6C63FF, #00D4FF); border-radius:4px; transition:width 0.3s ease;"></div>
            </div>
            <span style="color:rgba(255,255,255,0.15); font-size:0.65rem; font-weight:600; min-width:35px;">{snr_db:.1f}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Visualizations
        st.markdown('<span class="sidebar-label">🔧 Visualizations</span>', unsafe_allow_html=True)
        show_trellis = st.checkbox("Trellis Diagram", value=True, key="show_trellis")
        show_ber_plot = st.checkbox("BER Performance", value=True, key="show_ber")
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Tech specs
        st.markdown("""
        <div class="sidebar-footer">
            <strong>⚡ Rate 1/2, K=3</strong><br>
            G₁ = 111 &nbsp;·&nbsp; G₂ = 101
        </div>
        """, unsafe_allow_html=True)
    
    return input_text, snr_db, show_trellis, show_ber_plot


def render_header():
    """Render premium main header with live status."""
    st.markdown("""
    <div class="main-header">
        <div class="main-title-group">
            <span class="main-title-icon">🔐</span>
            <span class="main-title-text">Convolutional Encoder &amp; Viterbi Decoder</span>
        </div>
        <div class="main-status-badge">
            <span class="main-status-dot"></span>
            <span class="main-status-text">Live · Real-time</span>
        </div>
    </div>
    <div class="main-subtitle">
        Interactive demonstration of forward error correction for digital communication
    </div>
    """, unsafe_allow_html=True)


def open_section(title, number, icon="📌", badge=""):
    """Open a premium section card."""
    st.markdown(f"""
    <div class="section-card">
        <div class="section-header">
            <span class="section-number">{number}</span>
            <span class="section-title">{icon} {title}</span>
            <span class="section-badge">{badge}</span>
        </div>
    """, unsafe_allow_html=True)


def close_section():
    """Close the section card."""
    st.markdown("</div>", unsafe_allow_html=True)


def render_bits(bits, label="Bitstream", icon="🔵", highlight_errors=None, highlight_flipped=None):
    """
    Render a premium colored bitstream with animations.
    """
    if highlight_errors is None:
        highlight_errors = []
    if highlight_flipped is None:
        highlight_flipped = []
    
    # Build HTML with colored bits
    bits_html = ""
    for i, b in enumerate(bits):
        classes = ["bit-0" if b == '0' else "bit-1"]
        
        if i in highlight_errors:
            classes.append("bit-error")
        if i in highlight_flipped:
            classes.append("bit-flipped")
        
        class_str = " ".join(classes)
        bits_html += f'<span class="{class_str}">{b}</span>'
    
    # Color for label dot
    dot_colors = {
        "🔵": "#4FC3F7",
        "📡": "#FF6B6B",
        "🔓": "#6C63FF"
    }
    dot_color = dot_colors.get(icon, "#4FC3F7")
    
    st.markdown(f"""
    <div class="bit-wrapper">
        <div class="bit-label">
            <span class="dot" style="background:{dot_color};"></span>
            {icon} {label}
        </div>
        <div class="bit-content">{bits_html}</div>
        <div class="bit-length">📏 {len(bits)} bits</div>
    </div>
    """, unsafe_allow_html=True)


def render_metrics(metrics):
    """
    Render premium metric cards.
    
    Args:
        metrics: List of dicts with keys: value, label, sub, color_class
    """
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            val_class = f"metric-value {metric.get('color_class', 'white')}"
            st.markdown(f"""
            <div class="metric-card">
                <div class="{val_class}">{metric['value']}</div>
                <div class="metric-label">{metric['label']}</div>
                {f'<div class="metric-sub">{metric["sub"]}</div>' if metric.get("sub") else ""}
            </div>
            """, unsafe_allow_html=True)


def render_badge(text, type="success"):
    """Render a premium status badge."""
    st.markdown(f'<span class="badge badge-{type}">{text}</span>', unsafe_allow_html=True)


def render_info_box(message, type="info"):
    """Render a premium info box."""
    st.markdown(f"""
    <div class="info-box {type}">
        {message}
    </div>
    """, unsafe_allow_html=True)


def render_legend():
    """Render the bit color legend."""
    st.markdown("""
    <div class="legend-container">
        <div class="legend-item">
            <span style="color:#4FC3F7;">0</span> — Bit 0
        </div>
        <div class="legend-item">
            <span style="color:#FFD54F;">1</span> — Bit 1
        </div>
        <div class="legend-item">
            <span style="background:rgba(255,107,107,0.3); padding:0 4px; border-radius:3px;">Flipped</span> — Noise-induced error
        </div>
        <div class="legend-item">
            <span style="background:rgba(255,107,107,0.2); padding:0 4px; border-radius:3px;">Error</span> — Decoding error
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_status_indicator(snr_db, ber, is_perfect):
    """Render a premium status indicator."""
    if is_perfect:
        st.markdown(f"""
        <div class="status-container success">
            <span class="status-icon">✅</span>
            <div class="status-text">
                <div class="status-title success">Perfect Recovery!</div>
                <div class="status-sub">All bits decoded correctly at SNR = {snr_db:.1f} dB</div>
            </div>
            <span class="status-metric success">BER = {ber:.6f}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-container warning">
            <span class="status-icon">⚠️</span>
            <div class="status-text">
                <div class="status-title warning">Some Errors Detected</div>
                <div class="status-sub">Try increasing SNR for better recovery</div>
            </div>
            <span class="status-metric warning">BER = {ber:.6f}</span>
        </div>
        """, unsafe_allow_html=True)


def render_trellis(trellis_path, state_labels=['00', '01', '10', '11']):
    """Render premium trellis diagram with dark theme."""
    if not trellis_path:
        st.info("No trellis data available")
        return
    
    fig = go.Figure()
    
    # Color palette
    state_colors = ['#6C63FF', '#4FC3F7', '#FF6B6B', '#FFD54F']
    
    # Draw state nodes with glow
    num_steps = len(trellis_path) + 1
    for step in range(num_steps):
        for state in range(4):
            fig.add_trace(go.Scatter(
                x=[step],
                y=[state],
                mode='markers',
                marker=dict(
                    size=20,
                    color=state_colors[state],
                    line=dict(width=2, color='rgba(255,255,255,0.05)'),
                    symbol='circle'
                ),
                showlegend=False,
                hoverinfo='text',
                text=f"Step {step}<br>State {state_labels[state]}"
            ))
    
    # Draw transitions
    path_x, path_y = [], []
    for i, transition in enumerate(trellis_path):
        from_state = transition['from_state']
        to_state = transition['to_state']
        input_bit = transition['input_bit']
        
        path_x.extend([i, i+1, None])
        path_y.extend([from_state, to_state, None])
        
        # Label
        mid_x = (i + i+1) / 2
        mid_y = (from_state + to_state) / 2
        fig.add_annotation(
            x=mid_x,
            y=mid_y + 0.35,
            text=f"b={input_bit}",
            showarrow=False,
            font=dict(size=11, color='rgba(255,255,255,0.4)', weight='bold'),
            bgcolor='rgba(8,8,26,0.85)',
            bordercolor='rgba(108,99,255,0.15)',
            borderwidth=1,
            borderpad=3
        )
    
    # Draw winning path
    fig.add_trace(go.Scatter(
        x=path_x,
        y=path_y,
        mode='lines+markers',
        line=dict(color='#6C63FF', width=4, shape='linear'),
        marker=dict(size=16, color='#6C63FF', symbol='diamond', 
                   line=dict(width=2, color='rgba(255,255,255,0.1)')),
        name='🏆 Winning Path',
        hoverinfo='text',
        text=[f"Step {i}" for i in range(len(path_x)) if path_x[i] is not None]
    ))
    
    fig.update_layout(
        title=dict(
            text="Maximum Likelihood Path Through Trellis",
            font=dict(color='rgba(255,255,255,0.5)', size=14, weight='600'),
            x=0.5
        ),
        xaxis_title=dict(text="Time Step", font=dict(color='rgba(255,255,255,0.15)')),
        yaxis_title=dict(text="State", font=dict(color='rgba(255,255,255,0.15)')),
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=state_labels,
            autorange='reversed',
            gridcolor='rgba(255,255,255,0.03)',
            zeroline=False,
            tickfont=dict(color='rgba(255,255,255,0.2)')
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.03)',
            zeroline=False,
            tickfont=dict(color='rgba(255,255,255,0.2)')
        ),
        height=400,
        showlegend=True,
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.4)', size=11),
        margin=dict(l=50, r=50, t=60, b=50),
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(8,8,26,0.8)',
            bordercolor='rgba(255,255,255,0.04)',
            borderwidth=1,
            font=dict(color='rgba(255,255,255,0.4)')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_ber_plot(snr_values, ber_values, theoretical_ber=None):
    """Render premium BER plot with dark theme."""
    
    fig, ax = plt.subplots(figsize=(12, 5.5))
    
    # Dark theme
    ax.set_facecolor('rgba(0,0,0,0)')
    fig.patch.set_facecolor('rgba(0,0,0,0)')
    
    # Simulated BER
    ax.semilogy(snr_values, ber_values, 'o-', 
               label='Simulated (Viterbi Decoded)', 
               markersize=8, 
               linewidth=2.5,
               color='#6C63FF',
               markerfacecolor='#6C63FF',
               markeredgecolor='rgba(108,99,255,0.2)',
               markeredgewidth=2)
    
    # Theoretical BER
    if theoretical_ber:
        ax.semilogy(snr_values, theoretical_ber, '--', 
                   label='Theoretical (Uncoded BPSK)', 
                   linewidth=2,
                   color='#FF6B6B',
                   alpha=0.5)
    
    # Styling
    ax.set_xlabel('SNR (dB)', fontsize=12, fontweight='600', color='rgba(255,255,255,0.4)')
    ax.set_ylabel('Bit Error Rate (BER)', fontsize=12, fontweight='600', color='rgba(255,255,255,0.4)')
    ax.set_title('BER Performance: Convolutional Coding vs Uncoded', 
                fontsize=14, fontweight='700', color='rgba(255,255,255,0.6)')
    
    ax.grid(True, alpha=0.05, linestyle='--')
    ax.tick_params(colors='rgba(255,255,255,0.15)', labelsize=9)
    
    # Set y-axis limits
    ax.set_ylim([1e-6, 1])
    
    # Legend
    legend = ax.legend(fontsize=10, loc='lower left', framealpha=0.9)
    legend.get_frame().set_facecolor('rgba(8,8,26,0.9)')
    legend.get_frame().set_edgecolor('rgba(255,255,255,0.04)')
    for text in legend.get_texts():
        text.set_color('rgba(255,255,255,0.4)')
    
    # Find coding gain
    if ber_values and min(ber_values) < 1e-3:
        for i, ber in enumerate(ber_values):
            if ber < 1e-3:
                ax.axhline(y=1e-3, color='rgba(255,255,255,0.05)', linestyle=':', alpha=0.5)
                ax.axvline(x=snr_values[i], color='rgba(255,255,255,0.05)', linestyle=':', alpha=0.5)
                coding_gain = snr_values[i] - 6.5
                ax.text(snr_values[i] + 0.3, 5e-4, 
                       f'Coding Gain ≈ {coding_gain:.1f} dB', 
                       fontsize=10,
                       color='rgba(255,255,255,0.3)',
                       bbox=dict(facecolor='rgba(8,8,26,0.9)', 
                                edgecolor='rgba(108,99,255,0.1)',
                                boxstyle='round,pad=0.4'))
                break
    
    st.pyplot(fig)
    plt.close(fig)


def render_ber_table(snr_values, ber_values, theoretical_ber=None):
    """Render BER data as a premium table."""
    data = {
        'SNR (dB)': snr_values,
        'BER (Simulated)': [f'{b:.2e}' for b in ber_values]
    }
    if theoretical_ber:
        data['BER (Theoretical)'] = [f'{b:.2e}' for b in theoretical_ber]
    
    df = pd.DataFrame(data)
    
    st.dataframe(
        df.style.background_gradient(
            subset=['BER (Simulated)'],
            cmap='viridis',
            low=0.1,
            high=0.3
        ).format({
            'SNR (dB)': '{:.1f}'
        }),
        use_container_width=True,
        height=280
    )


def render_compare_bits(original, received, decoded, flipped_indices=None):
    """
    Render a premium side-by-side comparison.
    """
    if flipped_indices is None:
        flipped_indices = []
    
    # Original
    render_bits(original, label="Original", icon="🔵", highlight_errors=[])
    
    # Received with flipped bits
    render_bits(received, label="Received (Noisy)", icon="📡", highlight_flipped=flipped_indices)
    
    # Decoded with errors
    error_indices = [i for i, (a, b) in enumerate(zip(original, decoded)) if a != b]
    render_bits(decoded, label="Decoded", icon="🔓", highlight_errors=error_indices)
    
    # Legend
    render_legend()
