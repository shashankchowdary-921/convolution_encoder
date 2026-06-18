"""
core/ui.py – Clean, professional UI components
No emojis, no gradients, no glassmorphism.
"""

import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

# ─── CSS ────────────────────────────────────────────────────────────────

def apply_custom_css():
    st.markdown("""
    <style>
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
        * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }

        /* Global */
        .stApp { background: #F8F7F4; }
        .main-container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

        /* Sidebar – slim, clean */
        [data-testid="stSidebar"] {
            background: #FFFFFF !important;
            border-right: 1px solid #E5E3E0 !important;
            padding: 24px 16px !important;
            width: 260px !important;
        }
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stSlider,
        [data-testid="stSidebar"] .stTextArea {
            background: transparent !important;
        }
        [data-testid="stSidebar"] .stTextArea textarea {
            border: 1px solid #E5E3E0 !important;
            border-radius: 8px !important;
            color: #111111 !important;
            background: #FFFFFF !important;
            font-size: 14px;
        }

        /* Headers */
        .app-title {
            font-size: 28px;
            font-weight: 700;
            color: #111111;
            letter-spacing: -0.3px;
            padding: 0 0 4px 0;
        }
        .app-subtitle {
            font-size: 16px;
            font-weight: 400;
            color: #888888;
            margin-bottom: 32px;
            border-bottom: 1px solid #E5E3E0;
            padding-bottom: 16px;
        }

        /* Pipeline */
        .pipeline-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #FFFFFF;
            border: 1px solid #E5E3E0;
            border-radius: 12px;
            padding: 16px 24px;
            margin: 16px 0 24px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }
        .pipeline-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            font-size: 13px;
            font-weight: 500;
            color: #555555;
        }
        .pipeline-step .label { font-weight: 600; color: #111111; }
        .pipeline-step .status {
            font-size: 11px;
            color: #888888;
            font-weight: 400;
        }
        .pipeline-arrow {
            color: #B0B0B0;
            font-size: 20px;
            font-weight: 300;
            user-select: none;
        }

        /* Summary cards */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin: 16px 0 24px 0;
        }
        .summary-card {
            background: #FFFFFF;
            border: 1px solid #E5E3E0;
            border-radius: 12px;
            padding: 16px 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            text-align: left;
        }
        .summary-card .value {
            font-size: 24px;
            font-weight: 700;
            color: #111111;
            line-height: 1.2;
        }
        .summary-card .label {
            font-size: 12px;
            font-weight: 500;
            color: #888888;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
        .summary-card .sub {
            font-size: 14px;
            color: #555555;
        }

        /* Tabs – clean, underline style */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            border-bottom: 1px solid #E5E3E0;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 14px;
            font-weight: 500;
            color: #555555;
            padding: 8px 0;
            border-bottom: 2px solid transparent;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: #4F46E5;
            border-bottom-color: #4F46E5;
        }

        /* Bit display – monospace, grouped */
        .bit-block {
            background: #F8F7F4;
            border: 1px solid #E5E3E0;
            border-radius: 8px;
            padding: 12px 16px;
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.8;
            overflow-x: auto;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .bit-block .bit-0 { color: #4F46E5; }  /* accent */
        .bit-block .bit-1 { color: #111111; }
        .bit-block .error { background: #FFE5E5; color: #B91C1C; border-radius: 2px; padding: 0 2px; }
        .bit-block .correct { background: #E5F9F0; color: #0B7C5E; border-radius: 2px; padding: 0 2px; }

        /* Trellis container – full width */
        .trellis-container {
            background: #FFFFFF;
            border: 1px solid #E5E3E0;
            border-radius: 12px;
            padding: 12px;
            margin: 12px 0;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .summary-grid { grid-template-columns: 1fr 1fr; }
            .pipeline-container { flex-wrap: wrap; gap: 8px; justify-content: center; }
            .app-title { font-size: 22px; }
        }
        @media (max-width: 480px) {
            .summary-grid { grid-template-columns: 1fr; }
        }
    </style>
    """, unsafe_allow_html=True)


# ─── COMPONENTS ──────────────────────────────────────────────────────────

def render_sidebar():
    """Return: input_text, snr_db, run_clicked, show_trellis, show_ber"""
    with st.sidebar:
        st.markdown("### Message")
        input_text = st.text_area(
            label="Message",
            value="Hello World",
            max_chars=200,
            label_visibility="hidden"   # label is non‑empty but hidden
        )

        st.markdown("### Signal-to-Noise Ratio")
        snr_db = st.slider(
            label="SNR (dB)",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.5,
            label_visibility="hidden"
        )

        run = st.button("Run Simulation", type="primary", use_container_width=True)

        st.markdown("---")
        show_trellis = st.checkbox("Show Trellis Diagram", value=True)
        show_ber = st.checkbox("Show BER Performance", value=True)

    return input_text, snr_db, run, show_trellis, show_ber


def render_header():
    st.markdown("""
    <div class="app-title">Convolutional Encoder &amp; Viterbi Decoder</div>
    <div class="app-subtitle">Interactive demonstration of forward error correction for digital communication</div>
    """, unsafe_allow_html=True)


def render_pipeline(stage):
    """
    stage: dict with keys: text, binary, encoded, snr, decoded, recovered
    """
    steps = [
        ("Text", stage.get("text", "—")),
        ("Binary", stage.get("binary", "—")),
        ("Encoder", stage.get("encoded", "—")),
        ("AWGN", f"{stage.get('snr', '—')} dB" if stage.get('snr') is not None else "—"),
        ("Viterbi", stage.get("decoded", "—")),
        ("Recovered", stage.get("recovered", "—"))
    ]
    html = '<div class="pipeline-container">'
    for i, (label, value) in enumerate(steps):
        html += f'''
        <div class="pipeline-step">
            <span class="label">{label}</span>
            <span class="status">{value}</span>
        </div>
        '''
        if i < len(steps)-1:
            html += '<span class="pipeline-arrow">→</span>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_summary(original, recovered, ber, errors_corrected, snr):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="summary-card">
            <div class="value">{original[:20]}{'…' if len(original)>20 else ''}</div>
            <div class="label">Original Text</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="summary-card">
            <div class="value">{recovered[:20]}{'…' if len(recovered)>20 else ''}</div>
            <div class="label">Recovered Text</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        ber_str = f"{ber:.6f}" if ber >= 1e-6 else f"{ber:.2e}"
        st.markdown(f"""
        <div class="summary-card">
            <div class="value">{ber_str}</div>
            <div class="label">Bit Error Rate (BER)</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="summary-card">
            <div class="value">{errors_corrected}</div>
            <div class="label">Errors Corrected</div>
        </div>
        """, unsafe_allow_html=True)


def render_bitstream(bits, label, highlight_errors=None, highlight_corrected=None):
    """
    Display bits grouped in bytes (8 bits).
    highlight_errors: indices of bits that are wrong (red)
    highlight_corrected: indices of bits that were corrected (green)
    """
    if highlight_errors is None:
        highlight_errors = []
    if highlight_corrected is None:
        highlight_corrected = []
    # Group into bytes
    groups = [bits[i:i+8] for i in range(0, len(bits), 8)]
    html = f'<div class="bit-block"><span style="font-weight:600; color:#888; font-size:12px;">{label}</span><br>'
    for byte_idx, group in enumerate(groups):
        if len(group) < 8:
            group = group.ljust(8, '0')
        bits_html = ''
        for i, ch in enumerate(group):
            idx = byte_idx*8 + i
            cls = 'bit-0' if ch == '0' else 'bit-1'
            if idx in highlight_errors:
                cls += ' error'
            elif idx in highlight_corrected:
                cls += ' correct'
            bits_html += f'<span class="{cls}">{ch}</span>'
        html += bits_html + ' '
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_trellis(trellis_path, state_labels=['00','01','10','11']):
    """Render clean trellis diagram with Plotly (white background, thin lines)."""
    if not trellis_path:
        st.info("No trellis data available.")
        return

    fig = go.Figure()
    num_steps = len(trellis_path) + 1
    state_colors = ['#4F46E5', '#6B7280', '#6B7280', '#6B7280']  # accent for start

    # Draw state nodes
    for step in range(num_steps):
        for state in range(4):
            fig.add_trace(go.Scatter(
                x=[step], y=[state],
                mode='markers',
                marker=dict(
                    size=16,
                    color=state_colors[state],
                    line=dict(width=1, color='#D1D5DB'),
                ),
                showlegend=False,
                hoverinfo='text',
                text=f"Step {step}<br>State {state_labels[state]}"
            ))

    # Draw edges (only survivor path for clarity; you could draw all, but we keep it simple)
    path_x, path_y = [], []
    for i, trans in enumerate(trellis_path):
        from_s = trans['from_state']
        to_s = trans['to_state']
        inp = trans['input_bit']
        path_x.extend([i, i+1, None])
        path_y.extend([from_s, to_s, None])
        # label
        mid_x = (i + i+1)/2
        mid_y = (from_s + to_s)/2
        fig.add_annotation(
            x=mid_x,
            y=mid_y + 0.25,
            text=f"{inp}",
            showarrow=False,
            font=dict(size=10, color='#4F46E5'),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='#E5E3E0',
            borderwidth=1,
            borderpad=2
        )

    # Survivor path
    fig.add_trace(go.Scatter(
        x=path_x, y=path_y,
        mode='lines+markers',
        line=dict(color='#4F46E5', width=3),
        marker=dict(size=12, color='#4F46E5', symbol='circle'),
        name='Survivor Path'
    ))

    # Clean layout – no weight string
    fig.update_layout(
        title=None,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickmode='linear',
            dtick=1,
            tickfont=dict(color='#888888', size=11)
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=[0,1,2,3],
            ticktext=state_labels,
            autorange='reversed',
            showgrid=True,
            gridcolor='#F0EFED',
            zeroline=False,
            tickfont=dict(color='#888888', size=11)
        ),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        font=dict(color='#555555', size=12),
        height=350,
        margin=dict(l=40, r=20, t=20, b=30),
        showlegend=False,
        hovermode='closest'
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_ber_plot(snr_values, ber_values, theoretical_ber=None):
    """Publication‑quality BER plot."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_facecolor('#FFFFFF')
    fig.patch.set_facecolor('#FFFFFF')

    ax.semilogy(snr_values, ber_values, 'o-',
                label='Simulated (Viterbi)',
                color='#4F46E5',
                markersize=6,
                linewidth=1.5)
    if theoretical_ber is not None:
        ax.semilogy(snr_values, theoretical_ber, '--',
                    label='Theoretical (uncoded)',
                    color='#6B7280',
                    linewidth=1.5)

    ax.set_xlabel('SNR (dB)', fontsize=12, color='#555555')
    ax.set_ylabel('Bit Error Rate (BER)', fontsize=12, color='#555555')
    ax.grid(True, linestyle='-', linewidth=0.5, color='#E5E3E0')
    ax.set_ylim([1e-6, 1])
    ax.tick_params(colors='#888888', labelsize=10)
    ax.legend(frameon=True, facecolor='white', edgecolor='#E5E3E0', fontsize=10)

    st.pyplot(fig)
    plt.close(fig)
    st.caption("Fig. 1: BER vs SNR for rate‑1/2, K=3 convolutional code.")


def render_overview_tab(stage):
    """Overview tab: show pipeline and summary again, plus some stats."""
    st.subheader("Process Pipeline")
    render_pipeline(stage)
    st.subheader("Key Metrics")
    cols = st.columns(4)
    with cols[0]:
        st.metric("Original Length", len(stage.get("binary","")))
    with cols[1]:
        st.metric("Encoded Length", len(stage.get("encoded","")))
    with cols[2]:
        st.metric("SNR", f"{stage.get('snr', '—')} dB")
    with cols[3]:
        st.metric("Decoded Bits", len(stage.get("decoded","")))


def render_bit_analysis(original_bits, received_bits, decoded_bits, flipped_indices, error_indices):
    """Show original, received, decoded in grouped blocks."""
    st.subheader("Bitstream Comparison")
    render_bitstream(original_bits, "Original", highlight_errors=[])
    render_bitstream(received_bits, "Received (Noisy)", highlight_errors=flipped_indices)
    render_bitstream(decoded_bits, "Decoded", highlight_errors=error_indices)
    # Legend
    st.markdown("""
    <div style="display:flex; gap:20px; font-size:13px; color:#555; margin-top:8px;">
        <span><span style="background:#FFE5E5; padding:0 4px; border-radius:2px;">Red</span> = flipped bit (noise)</span>
        <span><span style="background:#E5F9F0; padding:0 4px; border-radius:2px;">Green</span> = corrected error</span>
    </div>
    """, unsafe_allow_html=True)
