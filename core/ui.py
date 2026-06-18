"""
core/ui.py - Premium UI Components for Convolutional Encoder & Viterbi Decoder
Modern dashboard design with glass-morphism, gradients, and animations.
"""

import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import time

# ============================================================================
# PREMIUM STYLING - Complete CSS Overhaul
# ============================================================================

def apply_custom_css():
    """Apply premium modern CSS styling."""
    st.markdown("""
    <style>
        /* ===== IMPORTS ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        
        /* ===== GLOBAL ===== */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 40%, #16213e 80%, #0a0a1a 100%);
            min-height: 100vh;
        }
        
        /* ===== SIDEBAR ===== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #0f0f23 100%) !important;
            border-right: 1px solid rgba(108, 99, 255, 0.15) !important;
            padding: 1rem 0.5rem !important;
        }
        
        [data-testid="stSidebar"] .sidebar-content {
            background: transparent !important;
        }
        
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stSlider,
        [data-testid="stSidebar"] .stTextArea {
            background: rgba(255, 255, 255, 0.03) !important;
            border-radius: 0.75rem !important;
            padding: 0.25rem !important;
        }
        
        /* ===== HEADERS ===== */
        .main-title {
            font-size: 3.2rem;
            font-weight: 900;
            background: linear-gradient(135deg, #6C63FF 0%, #00D4FF 50%, #FF6B6B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            padding: 1.5rem 0 0.5rem 0;
            letter-spacing: -0.5px;
            text-shadow: 0 0 80px rgba(108, 99, 255, 0.15);
        }
        
        .main-subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.5);
            font-size: 1.1rem;
            font-weight: 400;
            letter-spacing: 0.3px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* ===== SECTION HEADERS ===== */
        .section-container {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 1.25rem;
            border: 1px solid rgba(255, 255, 255, 0.06);
            padding: 1.5rem 1.75rem;
            margin: 1.5rem 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .section-container:hover {
            border-color: rgba(108, 99, 255, 0.2);
            box-shadow: 0 8px 48px rgba(108, 99, 255, 0.08);
        }
        
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
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            font-weight: 800;
            box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
        }
        
        .section-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.3px;
        }
        
        .section-subtitle {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.35);
            font-weight: 400;
            margin-left: auto;
            letter-spacing: 0.5px;
        }
        
        /* ===== BIT DISPLAY ===== */
        .bit-container {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 1rem;
            padding: 1.25rem 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.06);
            margin: 0.5rem 0;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            font-size: 1rem;
            line-height: 1.9;
            letter-spacing: 0.5px;
            position: relative;
            transition: all 0.3s ease;
        }
        
        .bit-container:hover {
            border-color: rgba(108, 99, 255, 0.2);
            box-shadow: 0 0 30px rgba(108, 99, 255, 0.05);
        }
        
        .bit-0 { color: #4FC3F7; }
        .bit-1 { color: #FFD54F; }
        
        .bit-error {
            background: rgba(255, 107, 107, 0.25);
            border-radius: 4px;
            padding: 0 3px;
            border-bottom: 2px solid #FF6B6B;
            animation: pulse-error 1.5s ease-in-out infinite;
        }
        
        .bit-flipped {
            background: rgba(255, 107, 107, 0.35);
            border-radius: 4px;
            padding: 0 3px;
            border-bottom: 2px solid #FF6B6B;
            animation: pulse-flipped 1s ease-in-out infinite;
        }
        
        @keyframes pulse-error {
            0%, 100% { background: rgba(255, 107, 107, 0.15); }
            50% { background: rgba(255, 107, 107, 0.35); }
        }
        
        @keyframes pulse-flipped {
            0%, 100% { background: rgba(255, 107, 107, 0.25); }
            50% { background: rgba(255, 107, 107, 0.5); }
        }
        
        .bit-label {
            display: inline-block;
            color: rgba(255, 255, 255, 0.4);
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
            padding: 0.2rem 0.75rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 2rem;
        }
        
        .bit-length {
            color: rgba(255, 255, 255, 0.25);
            font-size: 0.75rem;
            text-align: right;
            margin-top: 0.3rem;
        }
        
        /* ===== METRIC CARDS ===== */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 0.75rem;
            margin: 0.75rem 0;
        }
        
        .metric-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 1rem;
            padding: 1rem 1.25rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: default;
        }
        
        .metric-card:hover {
            transform: translateY(-3px) scale(1.02);
            border-color: rgba(108, 99, 255, 0.2);
            box-shadow: 0 8px 30px rgba(108, 99, 255, 0.1);
        }
        
        .metric-value {
            font-size: 1.6rem;
            font-weight: 800;
            line-height: 1.2;
            letter-spacing: -0.5px;
        }
        
        .metric-value.primary { 
            background: linear-gradient(135deg, #6C63FF, #00D4FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .metric-value.success { color: #00D4FF; }
        .metric-value.warning { color: #FFD54F; }
        .metric-value.danger { color: #FF6B6B; }
        .metric-value.gold { 
            background: linear-gradient(135deg, #FFD54F, #FF9A56);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .metric-value.white { color: #FFFFFF; }
        
        .metric-label {
            font-size: 0.6rem;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.35);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-top: 0.25rem;
        }
        
        .metric-sub {
            font-size: 0.7rem;
            color: rgba(255, 255, 255, 0.2);
            margin-top: 0.1rem;
        }
        
        /* ===== BADGES ===== */
        .badge {
            display: inline-block;
            padding: 0.3rem 1.2rem;
            border-radius: 2rem;
            font-weight: 700;
            font-size: 0.8rem;
            letter-spacing: 0.3px;
        }
        
        .badge-success {
            background: linear-gradient(135deg, #00D4FF, #00C9A7);
            color: #0a0a1a;
        }
        
        .badge-warning {
            background: linear-gradient(135deg, #FFD54F, #FF9A56);
            color: #0a0a1a;
        }
        
        .badge-danger {
            background: linear-gradient(135deg, #FF6B6B, #FF3366);
            color: white;
        }
        
        .badge-info {
            background: linear-gradient(135deg, #6C63FF, #4FC3F7);
            color: white;
        }
        
        .badge-gold {
            background: linear-gradient(135deg, #FFD54F, #FF9A56);
            color: #0a0a1a;
        }
        
        /* ===== INFO BOXES ===== */
        .info-box {
            padding: 0.75rem 1.25rem;
            border-radius: 0.75rem;
            margin: 0.5rem 0;
            font-weight: 500;
            border-left: 4px solid;
        }
        
        .info-box.success {
            background: rgba(0, 212, 255, 0.08);
            border-color: #00D4FF;
            color: #00D4FF;
        }
        
        .info-box.warning {
            background: rgba(255, 213, 79, 0.08);
            border-color: #FFD54F;
            color: #FFD54F;
        }
        
        .info-box.danger {
            background: rgba(255, 107, 107, 0.08);
            border-color: #FF6B6B;
            color: #FF6B6B;
        }
        
        .info-box.info {
            background: rgba(108, 99, 255, 0.08);
            border-color: #6C63FF;
            color: #6C63FF;
        }
        
        /* ===== LEGEND ===== */
        .legend-container {
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin: 0.75rem 0;
            padding: 0.75rem 1rem;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 0.75rem;
            border: 1px solid rgba(255, 255, 255, 0.04);
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.5);
        }
        
        .legend-swatch {
            width: 16px;
            height: 16px;
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* ===== SIDEBAR STYLES ===== */
        .sidebar-title {
            color: #FFFFFF;
            font-size: 1.4rem;
            font-weight: 800;
            text-align: center;
            padding: 0.5rem 0 0.25rem 0;
            background: linear-gradient(135deg, #6C63FF, #00D4FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .sidebar-divider {
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            margin: 1rem 0;
        }
        
        .sidebar-label {
            color: rgba(255, 255, 255, 0.4);
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 0.25rem;
        }
        
        .sidebar-footer {
            color: rgba(255, 255, 255, 0.15);
            font-size: 0.7rem;
            text-align: center;
            margin-top: 1.5rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            line-height: 1.6;
        }
        
        .sidebar-footer strong {
            color: rgba(255, 255, 255, 0.3);
        }
        
        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(108, 99, 255, 0.3);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(108, 99, 255, 0.5);
        }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .main-title { font-size: 2rem; }
            .section-container { padding: 1rem; }
            .metric-grid { grid-template-columns: 1fr 1fr; }
            .bit-container { font-size: 0.7rem; padding: 0.75rem; }
        }
        
        @media (max-width: 480px) {
            .metric-grid { grid-template-columns: 1fr; }
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# PREMIUM COMPONENT FUNCTIONS
# ============================================================================

def render_sidebar():
    """Render premium sidebar with glass-morphism."""
    with st.sidebar:
        st.markdown('<div class="sidebar-title">🎛️ Control Panel</div>', unsafe_allow_html=True)
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Message Input
        st.markdown('<div class="sidebar-label">📝 Message</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="sidebar-label">📡 Signal-to-Noise Ratio</div>', unsafe_allow_html=True)
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
        
        # Display current SNR with visual indicator
        snr_percent = min(snr_db / 15.0 * 100, 100)
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.75rem; margin-top:0.25rem;">
            <div style="flex:1; height:4px; background:rgba(255,255,255,0.06); border-radius:4px; overflow:hidden;">
                <div style="width:{snr_percent}%; height:100%; background:linear-gradient(90deg, #FF6B6B, #FFD54F, #00D4FF); border-radius:4px; transition:width 0.3s ease;"></div>
            </div>
            <span style="color:rgba(255,255,255,0.3); font-size:0.7rem; font-weight:600;">{snr_db:.1f} dB</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Options
        st.markdown('<div class="sidebar-label">🔧 Visualizations</div>', unsafe_allow_html=True)
        show_trellis = st.checkbox("Trellis Diagram", value=True, key="show_trellis")
        show_ber_plot = st.checkbox("BER Performance", value=True, key="show_ber")
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div class="sidebar-footer">
            <strong>⚡ Rate 1/2, K=3</strong><br>
            G₁ = 111 &nbsp;·&nbsp; G₂ = 101
        </div>
        """, unsafe_allow_html=True)
    
    return input_text, snr_db, show_trellis, show_ber_plot


def render_header():
    """Render premium main header."""
    st.markdown("""
    <div class="main-title">🔐 Convolutional Encoder &amp; Viterbi Decoder</div>
    <div class="main-subtitle">
        Interactive demonstration of forward error correction for digital communication
    </div>
    """, unsafe_allow_html=True)


def render_section(title, number, icon="📌", subtitle=""):
    """Render a premium section container with header."""
    st.markdown(f"""
    <div class="section-container">
        <div class="section-header">
            <span class="section-number">{number}</span>
            <span class="section-title">{icon} {title}</span>
            <span class="section-subtitle">{subtitle}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Return the div opening so content can be placed inside
    return True


def close_section():
    """Close the section container div."""
    st.markdown("</div>", unsafe_allow_html=True)


def render_bits(bits, label="Bitstream", highlight_errors=None, highlight_flipped=None, key_prefix=""):
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
    
    # Add position markers every 8 bits for readability
    formatted_bits = ""
    for i, char in enumerate(bits_html):
        formatted_bits += char
        if (i + 1) % 24 == 0:  # Every 24 bits (3 bytes), add a small space
            formatted_bits += ' '
    
    st.markdown(f"""
    <div>
        <div class="bit-label">{label}</div>
        <div class="bit-container">{bits_html}</div>
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
            <span style="background:rgba(255,107,107,0.35); padding:0 4px; border-radius:3px;">Flipped</span> — Noise-induced error
        </div>
        <div class="legend-item">
            <span style="background:rgba(255,107,107,0.25); padding:0 4px; border-radius:3px;">Error</span> — Decoding error
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_trellis(trellis_path, state_labels=['00', '01', '10', '11']):
    """Render premium trellis diagram with modern styling."""
    if not trellis_path:
        st.info("No trellis data available")
        return
    
    fig = go.Figure()
    
    # Color palette
    colors = ['#6C63FF', '#00D4FF', '#FF6B6B', '#FFD54F']
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
                    size=18,
                    color=state_colors[state],
                    line=dict(width=2, color='rgba(255,255,255,0.1)'),
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
            font=dict(size=11, color='rgba(255,255,255,0.7)', weight='bold'),
            bgcolor='rgba(10,10,26,0.8)',
            bordercolor='rgba(108,99,255,0.3)',
            borderwidth=1,
            borderpad=3
        )
    
    # Draw winning path
    fig.add_trace(go.Scatter(
        x=path_x,
        y=path_y,
        mode='lines+markers',
        line=dict(color='#6C63FF', width=4, shape='linear'),
        marker=dict(size=14, color='#6C63FF', symbol='diamond'),
        name='🏆 Winning Path',
        hoverinfo='text',
        text=[f"Step {i}" for i in range(len(path_x)) if path_x[i] is not None]
    ))
    
    fig.update_layout(
        title=dict(
            text="Maximum Likelihood Path Through Trellis",
            font=dict(color='rgba(255,255,255,0.8)', size=16, weight='bold'),
            x=0.5
        ),
        xaxis_title=dict(text="Time Step", font=dict(color='rgba(255,255,255,0.4)')),
        yaxis_title=dict(text="State", font=dict(color='rgba(255,255,255,0.4)')),
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=state_labels,
            autorange='reversed',
            gridcolor='rgba(255,255,255,0.05)',
            zeroline=False
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.05)',
            zeroline=False
        ),
        height=450,
        showlegend=True,
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='rgba(255,255,255,0.6)', size=12),
        margin=dict(l=50, r=50, t=60, b=50),
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(10,10,26,0.8)',
            bordercolor='rgba(255,255,255,0.06)',
            borderwidth=1,
            font=dict(color='rgba(255,255,255,0.6)')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_ber_plot(snr_values, ber_values, theoretical_ber=None):
    """Render premium BER plot with modern styling."""
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Dark theme for plot
    ax.set_facecolor('#0a0a1a')
    fig.patch.set_facecolor('#0a0a1a')
    
    # Simulated BER
    ax.semilogy(snr_values, ber_values, 'o-', 
               label='Simulated (Viterbi Decoded)', 
               markersize=8, 
               linewidth=2.5,
               color='#6C63FF',
               markerfacecolor='#6C63FF',
               markeredgecolor='rgba(108,99,255,0.3)',
               markeredgewidth=2)
    
    # Theoretical BER
    if theoretical_ber:
        ax.semilogy(snr_values, theoretical_ber, '--', 
                   label='Theoretical (Uncoded BPSK)', 
                   linewidth=2,
                   color='#FF6B6B',
                   alpha=0.7)
    
    # Styling
    ax.set_xlabel('SNR (dB)', fontsize=13, fontweight='600', color='rgba(255,255,255,0.7)')
    ax.set_ylabel('Bit Error Rate (BER)', fontsize=13, fontweight='600', color='rgba(255,255,255,0.7)')
    ax.set_title('BER Performance: Convolutional Coding vs Uncoded', fontsize=15, fontweight='700', color='rgba(255,255,255,0.8)')
    
    ax.grid(True, alpha=0.1, linestyle='--')
    ax.tick_params(colors='rgba(255,255,255,0.3)', labelsize=10)
    
    # Set y-axis limits
    ax.set_ylim([1e-6, 1])
    
    # Legend
    legend = ax.legend(fontsize=11, loc='lower left', framealpha=0.9)
    legend.get_frame().set_facecolor('#0a0a1a')
    legend.get_frame().set_edgecolor('rgba(255,255,255,0.1)')
    for text in legend.get_texts():
        text.set_color('rgba(255,255,255,0.7)')
    
    # Find coding gain at BER = 1e-3
    if ber_values and min(ber_values) < 1e-3:
        for i, ber in enumerate(ber_values):
            if ber < 1e-3:
                ax.axhline(y=1e-3, color='rgba(255,255,255,0.2)', linestyle=':', alpha=0.5)
                ax.axvline(x=snr_values[i], color='rgba(255,255,255,0.2)', linestyle=':', alpha=0.5)
                coding_gain = snr_values[i] - 6.5
                ax.text(snr_values[i] + 0.3, 5e-4, 
                       f'Coding Gain ≈ {coding_gain:.1f} dB', 
                       fontsize=11,
                       color='rgba(255,255,255,0.7)',
                       bbox=dict(facecolor='rgba(10,10,26,0.9)', 
                                edgecolor='rgba(108,99,255,0.3)',
                                boxstyle='round,pad=0.5'))
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
    
    # Style the dataframe
    styled_df = df.style.background_gradient(
        subset=['BER (Simulated)'],
        cmap='coolwarm',
        low=0.3,
        high=0.7
    ).format({
        'SNR (dB)': '{:.1f}'
    })
    
    st.dataframe(styled_df, use_container_width=True, height=300)


def render_compare_bits(original, received, decoded, flipped_indices=None):
    """
    Render a premium side-by-side comparison of bitstreams.
    """
    if flipped_indices is None:
        flipped_indices = []
    
    # Show original
    render_bits(original, label="🔵 Original", highlight_errors=[])
    
    # Show received with flipped bits
    render_bits(received, label="📡 Received (Noisy)", highlight_flipped=flipped_indices)
    
    # Show decoded with errors
    error_indices = [i for i, (a, b) in enumerate(zip(original, decoded)) if a != b]
    render_bits(decoded, label="🔓 Decoded", highlight_errors=error_indices)
    
    # Show legend
    render_legend()


def render_status_indicator(snr_db, ber, is_perfect):
    """Render a premium status indicator."""
    if is_perfect:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:1rem; padding:0.75rem 1.25rem; background:rgba(0,212,255,0.08); border-radius:0.75rem; border:1px solid rgba(0,212,255,0.15);">
            <span style="font-size:2rem;">✅</span>
            <div>
                <div style="font-weight:700; color:#00D4FF;">Perfect Recovery!</div>
                <div style="font-size:0.8rem; color:rgba(255,255,255,0.3);">All bits decoded correctly at SNR = {snr_db:.1f} dB</div>
            </div>
            <span style="margin-left:auto; color:#00D4FF; font-weight:600; font-size:0.9rem;">BER = {ber:.6f}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:1rem; padding:0.75rem 1.25rem; background:rgba(255,107,107,0.08); border-radius:0.75rem; border:1px solid rgba(255,107,107,0.15);">
            <span style="font-size:2rem;">⚠️</span>
            <div>
                <div style="font-weight:700; color:#FF6B6B;">Some Errors Detected</div>
                <div style="font-size:0.8rem; color:rgba(255,255,255,0.3);">Try increasing SNR for better recovery</div>
            </div>
            <span style="margin-left:auto; color:#FF6B6B; font-weight:600; font-size:0.9rem;">BER = {ber:.6f}</span>
        </div>
        """, unsafe_allow_html=True)
