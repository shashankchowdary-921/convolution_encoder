"""
core/ui.py - All UI Components, Styling, and Layout Functions
This module separates presentation from logic for clean, maintainable code.
"""

import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

# ============================================================================
# STYLING - Custom CSS
# ============================================================================

def apply_custom_css():
    """Apply all custom CSS styles to the app."""
    st.markdown("""
    <style>
        /* ---------- Main Colors ---------- */
        :root {
            --primary: #6C63FF;
            --primary-dark: #5A52D5;
            --secondary: #FF6B6B;
            --success: #00C9A7;
            --warning: #FFC107;
            --dark: #1E1E2E;
            --light: #F8F9FE;
            --gray: #6C757D;
            --border: #E8EAF6;
        }
        
        /* ---------- Main Header ---------- */
        .main-header {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6C63FF 0%, #FF6B6B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            padding: 1.5rem 0 0.5rem 0;
            letter-spacing: -0.5px;
        }
        .main-subheader {
            text-align: center;
            color: var(--gray);
            font-size: 1.1rem;
            margin-bottom: 2rem;
            font-weight: 400;
            border-bottom: 2px solid var(--border);
            padding-bottom: 1rem;
        }
        
        /* ---------- Section Headers ---------- */
        .section-header {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--dark);
            padding: 0.6rem 1.2rem;
            background: var(--light);
            border-radius: 0.75rem;
            border-left: 5px solid var(--primary);
            margin: 2rem 0 1rem 0;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .section-number {
            background: var(--primary);
            color: white;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
            font-weight: 700;
        }
        
        /* ---------- Bit Display ---------- */
        .bit-container {
            background: #1A1A2E;
            border-radius: 1rem;
            padding: 1.25rem 1.5rem;
            border: 1px solid #2D2D44;
            margin: 0.5rem 0;
            position: relative;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            font-size: 0.95rem;
            line-height: 1.8;
            letter-spacing: 0.5px;
        }
        .bit-container .bit-0 { color: #4FC3F7; }
        .bit-container .bit-1 { color: #FFD54F; }
        .bit-container .bit-error {
            background: rgba(255, 107, 107, 0.25);
            border-radius: 3px;
            padding: 0 2px;
        }
        .bit-container .bit-flipped {
            background: rgba(255, 107, 107, 0.4);
            border-radius: 3px;
            padding: 0 2px;
            border-bottom: 2px solid var(--secondary);
        }
        .bit-label {
            display: inline-block;
            color: var(--gray);
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }
        
        /* ---------- Metric Cards ---------- */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin: 0.5rem 0 1rem 0;
        }
        .metric-card {
            background: white;
            border-radius: 1rem;
            padding: 1rem 1.25rem;
            text-align: center;
            border: 1px solid var(--border);
            box-shadow: 0 2px 8px rgba(108, 99, 255, 0.06);
            transition: all 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(108, 99, 255, 0.1);
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--dark);
            line-height: 1.2;
        }
        .metric-value.success { color: var(--success); }
        .metric-value.warning { color: var(--warning); }
        .metric-value.danger { color: var(--secondary); }
        .metric-value.primary { color: var(--primary); }
        .metric-label {
            font-size: 0.7rem;
            font-weight: 600;
            color: var(--gray);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 0.25rem;
        }
        .metric-sub {
            font-size: 0.85rem;
            color: var(--gray);
            margin-top: 0.1rem;
        }
        
        /* ---------- Status Badges ---------- */
        .badge {
            display: inline-block;
            padding: 0.25rem 1rem;
            border-radius: 2rem;
            font-weight: 700;
            font-size: 0.9rem;
        }
        .badge-success {
            background: #00C9A7;
            color: white;
        }
        .badge-warning {
            background: #FFC107;
            color: #1A1A2E;
        }
        .badge-danger {
            background: #FF6B6B;
            color: white;
        }
        .badge-info {
            background: #4FC3F7;
            color: #1A1A2E;
        }
        
        /* ---------- Info Boxes ---------- */
        .info-box {
            background: #F0F4FF;
            border-left: 4px solid var(--primary);
            padding: 0.75rem 1.25rem;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
            color: var(--dark);
        }
        .info-box.success {
            background: #E6F9F5;
            border-color: var(--success);
        }
        .info-box.warning {
            background: #FFF8E1;
            border-color: var(--warning);
        }
        .info-box.danger {
            background: #FFEBEE;
            border-color: var(--secondary);
        }
        
        /* ---------- Sidebar ---------- */
        .sidebar-section {
            padding: 0.5rem 0;
        }
        .sidebar-section h4 {
            color: var(--dark);
            font-weight: 700;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }
        .sidebar-divider {
            border: none;
            border-top: 2px solid var(--border);
            margin: 1rem 0;
        }
        .sidebar-footer {
            color: var(--gray);
            font-size: 0.75rem;
            text-align: center;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
        }
        .sidebar-footer strong {
            color: var(--dark);
        }
        
        /* ---------- Responsive Fixes ---------- */
        @media (max-width: 640px) {
            .main-header { font-size: 2rem; }
            .metric-grid { grid-template-columns: 1fr 1fr; }
            .bit-container { font-size: 0.75rem; padding: 0.75rem; }
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# COMPONENT FUNCTIONS
# ============================================================================

def render_sidebar():
    """Render the sidebar controls."""
    with st.sidebar:
        st.markdown("### 🎛️ Control Panel")
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        st.markdown("#### 📝 Message")
        input_text = st.text_area(
            "Enter your message:",
            value="Hello World",
            max_chars=200,
            help="Type any text message to encode and transmit",
            label_visibility="collapsed"
        )
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        st.markdown("#### 📡 Channel")
        snr_db = st.slider(
            "Signal-to-Noise Ratio (dB)",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.5,
            help="Higher SNR = less noise = better recovery"
        )
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        st.markdown("#### 🔧 Options")
        show_trellis = st.checkbox("Show Trellis Diagram", value=True)
        show_ber_plot = st.checkbox("Show BER Analysis", value=True)
        
        st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-footer">
            <strong>⚡ Rate 1/2, K=3</strong><br>
            G₁ = 111, G₂ = 101
        </div>
        """, unsafe_allow_html=True)
    
    return input_text, snr_db, show_trellis, show_ber_plot


def render_header():
    """Render the main page header."""
    st.markdown("""
    <div class="main-header">🔐 Convolutional Encoder &amp; Viterbi Decoder</div>
    <div class="main-subheader">
        Interactive demonstration of forward error correction for digital communication
    </div>
    """, unsafe_allow_html=True)


def render_section(title, number, icon="📌"):
    """Render a section header with number."""
    st.markdown(f"""
    <div class="section-header">
        <span class="section-number">{number}</span>
        {icon} {title}
    </div>
    """, unsafe_allow_html=True)


def render_bits(bits, label="Bitstream", highlight_errors=None, highlight_flipped=None):
    """
    Render a colored bitstream.
    
    Args:
        bits: Binary string
        label: Label text above the bitstream
        highlight_errors: List of indices where bits are wrong (for red highlight)
        highlight_flipped: List of indices where bits were flipped by noise
    """
    if highlight_errors is None:
        highlight_errors = []
    if highlight_flipped is None:
        highlight_flipped = []
    
    # Build HTML with colored bits
    bits_html = ""
    for i, b in enumerate(bits):
        classes = []
        if b == '0':
            classes.append("bit-0")
        else:
            classes.append("bit-1")
        
        if i in highlight_errors:
            classes.append("bit-error")
        if i in highlight_flipped:
            classes.append("bit-flipped")
        
        class_str = " ".join(classes)
        bits_html += f'<span class="{class_str}">{b}</span>'
    
    st.markdown(f"""
    <div>
        <div class="bit-label">{label}</div>
        <div class="bit-container">{bits_html}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show length
    st.caption(f"📏 Length: {len(bits)} bits")


def render_metrics(metrics):
    """
    Render a grid of metric cards.
    
    Args:
        metrics: List of dicts with keys: value, label, sub, color_class
    """
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            val_class = f"metric-value {metric.get('color_class', 'primary')}"
            st.markdown(f"""
            <div class="metric-card">
                <div class="{val_class}">{metric['value']}</div>
                <div class="metric-label">{metric['label']}</div>
                {f'<div class="metric-sub">{metric["sub"]}</div>' if metric.get("sub") else ""}
            </div>
            """, unsafe_allow_html=True)


def render_badge(text, type="success"):
    """Render a status badge."""
    st.markdown(f'<span class="badge badge-{type}">{text}</span>', unsafe_allow_html=True)


def render_info_box(message, type="info"):
    """Render an info box."""
    st.markdown(f"""
    <div class="info-box {type}">
        {message}
    </div>
    """, unsafe_allow_html=True)


def render_trellis(trellis_path, state_labels=['00', '01', '10', '11']):
    """Render the trellis diagram using Plotly."""
    if not trellis_path:
        return
    
    fig = go.Figure()
    
    # Draw state nodes
    num_steps = len(trellis_path) + 1
    colors = ['#D1D5DB', '#9CA3AF', '#6B7280', '#4B5563']
    
    for step in range(num_steps):
        for state in range(4):
            fig.add_trace(go.Scatter(
                x=[step],
                y=[state],
                mode='markers',
                marker=dict(size=16, color=colors[state], line=dict(width=2, color='white')),
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
        
        # Path coordinates
        path_x.extend([i, i+1, None])
        path_y.extend([from_state, to_state, None])
        
        # Label
        mid_x = (i + i+1) / 2
        mid_y = (from_state + to_state) / 2
        fig.add_annotation(
            x=mid_x,
            y=mid_y + 0.3,
            text=f"b={input_bit}",
            showarrow=False,
            font=dict(size=11, color='#6C63FF', weight='bold'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#6C63FF',
            borderwidth=1,
            borderpad=2
        )
        
        # Draw all possible transitions (faint)
        for fb in [0, 1]:
            if fb != input_bit:
                # Faint ghost paths
                fig.add_trace(go.Scatter(
                    x=[i, i+1],
                    y=[from_state, to_state],
                    mode='lines',
                    line=dict(color='rgba(200,200,200,0.2)', width=1, dash='dot'),
                    showlegend=False,
                    hoverinfo='skip'
                ))
    
    # Draw winning path
    fig.add_trace(go.Scatter(
        x=path_x,
        y=path_y,
        mode='lines+markers',
        line=dict(color='#6C63FF', width=4),
        marker=dict(size=14, color='#6C63FF', symbol='diamond'),
        name='🏆 Winning Path',
        hoverinfo='text',
        text=[f"Step {i}" for i in range(len(path_x)) if path_x[i] is not None]
    ))
    
    fig.update_layout(
        title="Maximum Likelihood Path Through Trellis",
        xaxis_title="Time Step",
        yaxis_title="State",
        yaxis=dict(
            tickmode='array',
            tickvals=[0, 1, 2, 3],
            ticktext=state_labels,
            autorange='reversed'
        ),
        height=450,
        showlegend=True,
        hovermode='closest',
        plot_bgcolor='white',
        font=dict(size=12),
        margin=dict(l=50, r=50, t=50, b=50),
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#E8EAF6',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_ber_plot(snr_values, ber_values, theoretical_ber=None):
    """Render the BER vs SNR plot."""
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Simulated BER
    ax.semilogy(snr_values, ber_values, 'o-', 
               label='Simulated (Viterbi Decoded)', 
               markersize=8, linewidth=2, color='#6C63FF')
    
    # Theoretical BER
    if theoretical_ber:
        ax.semilogy(snr_values, theoretical_ber, '--', 
                   label='Theoretical (Uncoded BPSK)', 
                   linewidth=2, color='#FF6B6B')
    
    ax.set_xlabel('SNR (dB)', fontsize=13, fontweight='600')
    ax.set_ylabel('Bit Error Rate (BER)', fontsize=13, fontweight='600')
    ax.set_title('BER Performance: Convolutional Coding vs Uncoded Transmission', fontsize=15)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=12, loc='lower left')
    ax.set_ylim([1e-6, 1])
    
    # Find coding gain at BER = 1e-3
    if ber_values and min(ber_values) < 1e-3:
        for i, ber in enumerate(ber_values):
            if ber < 1e-3:
                ax.axhline(y=1e-3, color='gray', linestyle=':', alpha=0.5)
                ax.axvline(x=snr_values[i], color='gray', linestyle=':', alpha=0.5)
                coding_gain = snr_values[i] - 6.5  # Approximate
                ax.text(snr_values[i] + 0.3, 5e-4, 
                       f'Coding Gain ≈ {coding_gain:.1f} dB', 
                       fontsize=11, 
                       bbox=dict(facecolor='white', alpha=0.9, edgecolor='#6C63FF', boxstyle='round,pad=0.3'))
                break
    
    st.pyplot(fig)
    plt.close(fig)


def render_ber_table(snr_values, ber_values, theoretical_ber=None):
    """Render BER data as a table."""
    data = {
        'SNR (dB)': snr_values,
        'BER (Simulated)': [f'{b:.2e}' for b in ber_values]
    }
    if theoretical_ber:
        data['BER (Theoretical)'] = [f'{b:.2e}' for b in theoretical_ber]
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_compare_bits(original, received, decoded, flipped_indices=None):
    """
    Render a side-by-side comparison of original, received, and decoded bits.
    """
    if flipped_indices is None:
        flipped_indices = []
    
    # Original
    render_bits(original, label="🔵 Original", highlight_errors=[])
    
    # Received (show flipped bits)
    render_bits(received, label="📡 Received (Noisy)", highlight_flipped=flipped_indices)
    
    # Decoded (show errors)
    error_indices = [i for i, (a, b) in enumerate(zip(original, decoded)) if a != b]
    render_bits(decoded, label="🔓 Decoded", highlight_errors=error_indices)
    
    # Legend
    st.markdown("""
    <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; margin: 0.5rem 0; font-size: 0.85rem;">
        <span>🟡 <span style="color: #FFD54F;">1</span> / <span style="color: #4FC3F7;">0</span> — Original bits</span>
        <span><span style="background: rgba(255,107,107,0.4); padding: 0 4px; border-radius: 3px;">Red background</span> — Bit flipped by noise</span>
        <span><span style="background: rgba(255,107,107,0.25); padding: 0 4px; border-radius: 3px;">Pink background</span> — Decoding error</span>
    </div>
    """, unsafe_allow_html=True)
