import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import math

from core.encoder import ConvolutionalEncoder
from core.decoder import ViterbiDecoder
from core.channel import AWGNChannel
from core.utils import text_to_bits, bits_to_text, calculate_ber

# ============================================================================
# Page Configuration - CHANGE YOUR TITLE HERE
# ============================================================================
st.set_page_config(
    page_title="Convolutional Encoder & Viterbi Decoder - Interactive Demo",
    page_icon="🔐",
    layout="wide"
)

# ============================================================================
# Custom CSS - Professional UI Styling
# ============================================================================
st.markdown("""
<style>
    /* Main header */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        padding: 0.75rem 1rem;
        background: linear-gradient(90deg, #f0f2f6 0%, #ffffff 100%);
        border-radius: 0.5rem;
        border-left: 5px solid #667eea;
        margin: 1.5rem 0 0.75rem 0;
    }
    
    /* Bit display - CRITICAL FIX: bits are now visible */
    .bit-display {
        font-family: 'Courier New', monospace;
        font-size: 0.95rem;
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        word-wrap: break-word;
        overflow-x: auto;
        white-space: pre-wrap;
        border: 1px solid #333;
        line-height: 1.6;
        letter-spacing: 0.5px;
    }
    
    .bit-display .bit-0 { color: #569cd6; }
    .bit-display .bit-1 { color: #d7ba7d; }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.25rem;
        border-radius: 0.75rem;
        text-align: center;
        border: 1px solid #dee2e6;
        transition: transform 0.2s;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Status badges */
    .badge-success {
        background: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-weight: 600;
    }
    .badge-warning {
        background: #ffc107;
        color: #212529;
        padding: 0.25rem 0.75rem;
        border-radius: 2rem;
        font-weight: 600;
    }
    
    /* Info boxes */
    .info-box {
        background: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 0.75rem 1.25rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Initialize Components
# ============================================================================
@st.cache_resource
def get_encoder():
    return ConvolutionalEncoder()

@st.cache_resource
def get_decoder():
    return ViterbiDecoder()

@st.cache_resource
def get_channel():
    return AWGNChannel()

encoder = get_encoder()
decoder = get_decoder()
channel = get_channel()

# ============================================================================
# Sidebar Controls
# ============================================================================
with st.sidebar:
    st.markdown("### 🎛️ Controls")
    
    st.markdown("---")
    st.markdown("#### 📝 Input Message")
    input_text = st.text_area(
        "Enter your message:",
        value="Hello World",
        max_chars=200,
        help="Type any text message to encode and transmit"
    )
    
    st.markdown("---")
    st.markdown("#### 📡 Channel Settings")
    snr_db = st.slider(
        "Signal-to-Noise Ratio (dB)",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.5,
        help="Higher SNR = less noise = better recovery"
    )
    
    st.markdown("---")
    st.markdown("#### 🔧 Advanced Options")
    show_trellis = st.checkbox("Show Trellis Diagram", value=True)
    show_ber_plot = st.checkbox("Show BER vs SNR Plot", value=True)
    
    st.markdown("---")
    st.caption("**⚡ Rate 1/2, K=3**")
    st.caption("G₁ = 111, G₂ = 101")

# ============================================================================
# Main Content - CHANGE YOUR TITLE HERE
# ============================================================================
st.markdown('<p class="main-header">🔐 Convolutional Encoder & Viterbi Decoder</p>', unsafe_allow_html=True)

# Subtitle
st.markdown(
    """
    <div style="text-align: center; color: #6c757d; margin-bottom: 2rem; font-size: 1.1rem;">
        Interactive demonstration of forward error correction for digital communication
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================================
# STEP 1: Text to Binary
# ============================================================================
st.markdown('<p class="section-header">📝 Step 1: Text → Binary</p>', unsafe_allow_html=True)

# Show original text
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("**Original Text:**")
    st.code(input_text, language="text")
with col2:
    st.markdown("**Binary (8-bit ASCII):**")
    binary = text_to_bits(input_text)
    # Color-coded binary display
    bits_html = ''.join([
        f'<span class="bit-{b}">{b}</span>' for b in binary
    ])
    st.markdown(f'<div class="bit-display">{bits_html}</div>', unsafe_allow_html=True)
    st.caption(f"📏 Length: {len(binary)} bits ({len(input_text)} characters × 8 bits)")

# ============================================================================
# STEP 2: Convolutional Encoding
# ============================================================================
st.markdown('<p class="section-header">⚙️ Step 2: Convolutional Encoding</p>', unsafe_allow_html=True)

with st.spinner("Encoding..."):
    encoded = encoder.encode(binary)

# Encoder parameters
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Code Rate</div>
        <div class="metric-value">1/2</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Constraint Length</div>
        <div class="metric-value">K = 3</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Generator Polynomials</div>
        <div class="metric-value" style="font-size:1.2rem;">G₁=111, G₂=101</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Encoded Length</div>
        <div class="metric-value">{len(encoded)}</div>
    </div>
    """, unsafe_allow_html=True)

# Display encoded bits
st.markdown("**Encoded Bitstream:**")
bits_html = ''.join([
    f'<span class="bit-{b}">{b}</span>' for b in encoded
])
st.markdown(f'<div class="bit-display">{bits_html}</div>', unsafe_allow_html=True)
st.caption(f"📏 Length: {len(encoded)} bits (Rate 1/2 expansion from {len(binary)} bits)")

# ============================================================================
# STEP 3: AWGN Channel
# ============================================================================
st.markdown('<p class="section-header">📡 Step 3: AWGN Channel</p>', unsafe_allow_html=True)

with st.spinner(f"Adding AWGN noise at SNR = {snr_db} dB..."):
    received, tx_symbols, rx_symbols = channel.transmit(encoded, snr_db)

# Channel metrics
errors = sum(1 for a, b in zip(encoded, received) if a != b)
error_rate = errors / len(encoded) if len(encoded) > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SNR</div>
        <div class="metric-value">{snr_db:.1f} dB</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Bits Flipped</div>
        <div class="metric-value" style="color: {'#28a745' if errors == 0 else '#dc3545'}">{errors}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Channel Error Rate</div>
        <div class="metric-value" style="color: {'#28a745' if error_rate < 0.01 else '#dc3545'}">{error_rate:.2%}</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    total_bits = len(encoded)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Bits Sent</div>
        <div class="metric-value">{total_bits}</div>
    </div>
    """, unsafe_allow_html=True)

# Display received (noisy) bits
st.markdown("**Received (Noisy) Bitstream:**")
bits_html = ''.join([
    f'<span class="bit-{b}" style="{"background:#ff6b6b33" if encoded[i] != b else ""}">{b}</span>'
    for i, b in enumerate(received)
])
st.markdown(f'<div class="bit-display">{bits_html}</div>', unsafe_allow_html=True)
st.caption("🟥 Red highlights indicate bits flipped by noise")

# ============================================================================
# STEP 4: Viterbi Decoding
# ============================================================================
st.markdown('<p class="section-header">🔍 Step 4: Viterbi Decoding</p>', unsafe_allow_html=True)

with st.spinner("Decoding with Viterbi algorithm..."):
    try:
        decoded_result = decoder.decode_with_trellis(received)
        decoded = decoded_result['output']
    except Exception as e:
        st.error(f"Decoding error: {e}")
        decoded = ""

# Display decoded bits
st.markdown("**Decoded Bitstream:**")
if decoded:
    bits_html = ''.join([
        f'<span class="bit-{b}" style="{"background:#ff6b6b33" if binary[i] != b else ""}">{b}</span>'
        for i, b in enumerate(decoded)
    ])
    st.markdown(f'<div class="bit-display">{bits_html}</div>', unsafe_allow_html=True)
    st.caption("🟥 Red highlights indicate decoding errors")
else:
    st.warning("Decoding failed. Please check your input.")

# ============================================================================
# STEP 5: Results
# ============================================================================
st.markdown('<p class="section-header">✅ Step 5: Results</p>', unsafe_allow_html=True)

recovered_text = bits_to_text(decoded) if decoded else "(decoding failed)"
ber = calculate_ber(binary, decoded) if binary and decoded else 1.0
is_perfect = recovered_text == input_text

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid {'#28a745' if is_perfect else '#dc3545'}">
        <div class="metric-label">Recovered Text</div>
        <div class="metric-value" style="font-size:1.5rem;">{recovered_text}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    color = "#28a745" if ber == 0 else ("#ffc107" if ber < 0.01 else "#dc3545")
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid {color}">
        <div class="metric-label">Bit Error Rate (BER)</div>
        <div class="metric-value" style="color:{color}">{ber:.6f}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    status = "✅ Perfect Recovery!" if is_perfect else "⚠️ Some Errors Remain"
    color = "#28a745" if is_perfect else "#ffc107"
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid {color}">
        <div class="metric-label">Status</div>
        <div class="metric-value" style="font-size:1.2rem; color:{color}">{status}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# TRELLIS DIAGRAM
# ============================================================================
if show_trellis and 'decoded_result' in locals() and decoded_result:
    st.markdown('<p class="section-header">🔱 Viterbi Decoder Trellis Path</p>', unsafe_allow_html=True)
    
    trellis_path = decoded_result['trellis_path']
    state_labels = ['00', '01', '10', '11']
    
    if trellis_path:
        fig = go.Figure()
        
        # Draw all state nodes
        num_steps = len(trellis_path) + 1
        for step in range(num_steps):
            for state in range(4):
                fig.add_trace(go.Scatter(
                    x=[step],
                    y=[state],
                    mode='markers',
                    marker=dict(size=14, color='#d1d5db'),
                    showlegend=False,
                    hoverinfo='text',
                    text=f"Step {step}<br>State {state_labels[state]}"
                ))
        
        # Draw the winning path
        path_x, path_y = [], []
        for i, transition in enumerate(trellis_path):
            from_state = transition['from_state']
            to_state = transition['to_state']
            input_bit = transition['input_bit']
            
            path_x.extend([i, i+1, None])
            path_y.extend([from_state, to_state, None])
            
            fig.add_annotation(
                x=(i + i+1) / 2,
                y=(from_state + to_state) / 2 + 0.25,
                text=f"b={input_bit}",
                showarrow=False,
                font=dict(size=11, color='#667eea')
            )
        
        fig.add_trace(go.Scatter(
            x=path_x,
            y=path_y,
            mode='lines+markers',
            line=dict(color='#667eea', width=4),
            marker=dict(size=12, color='#667eea'),
            name='Winning Path'
        ))
        
        fig.update_layout(
            title="Maximum Likelihood Path Through the Trellis",
            xaxis_title="Time Step",
            yaxis_title="State",
            yaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3],
                ticktext=state_labels
            ),
            height=450,
            showlegend=True,
            hovermode='closest',
            plot_bgcolor='white',
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# BER vs SNR PLOT
# ============================================================================
if show_ber_plot:
    st.markdown('<p class="section-header">📊 BER Performance Analysis</p>', unsafe_allow_html=True)
    
    with st.spinner("Running BER analysis... This may take a moment..."):
        snr_values = np.arange(0, 11, 0.5)
        ber_values = []
        
        progress_bar = st.progress(0)
        for idx, snr in enumerate(snr_values):
            rx, _, _ = channel.transmit(encoded, snr)
            try:
                dec = decoder.decode(rx)
                ber_values.append(calculate_ber(binary, dec))
            except:
                ber_values.append(1.0)
            progress_bar.progress((idx + 1) / len(snr_values))
        progress_bar.empty()
        
        def q_function(x):
            return 0.5 * (1 - math.erf(x / np.sqrt(2)))
        
        theoretical_ber = [q_function(np.sqrt(10 ** (snr/10))) for snr in snr_values]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Simulated BER
        ax.semilogy(snr_values, ber_values, 'bo-', 
                   label='Simulated (Viterbi Decoded)', 
                   markersize=8, linewidth=2, color='#667eea')
        
        # Theoretical BER
        ax.semilogy(snr_values, theoretical_ber, 'r--', 
                   label='Theoretical (Uncoded BPSK)', 
                   linewidth=2, color='#dc3545')
        
        ax.set_xlabel('SNR (dB)', fontsize=13, fontweight='600')
        ax.set_ylabel('Bit Error Rate (BER)', fontsize=13, fontweight='600')
        ax.set_title('BER vs SNR: Convolutional Coding vs Uncoded Transmission', fontsize=15)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=12, loc='lower left')
        ax.set_ylim([1e-6, 1])
        
        # Shade the coding gain region
        if len(ber_values) > 0 and ber_values[0] < 1:
            for i, ber in enumerate(ber_values):
                if ber < 1e-3:
                    ax.axhline(y=1e-3, color='gray', linestyle=':', alpha=0.5)
                    ax.axvline(x=snr_values[i], color='gray', linestyle=':', alpha=0.5)
                    ax.text(snr_values[i] + 0.3, 5e-4, f'Coding Gain ≈ {snr_values[i] - 6.5:.1f} dB', 
                           fontsize=11, bbox=dict(facecolor='white', alpha=0.8))
                    break
        
        st.pyplot(fig)
        plt.close(fig)
        
        # Data table
        with st.expander("📋 View BER Data Table"):
            ber_df = pd.DataFrame({
                'SNR (dB)': snr_values,
                'BER (Simulated)': ber_values,
                'BER (Theoretical)': theoretical_ber
            })
            st.dataframe(ber_df.style.format({
                'BER (Simulated)': '{:.2e}',
                'BER (Theoretical)': '{:.2e}'
            }), use_container_width=True)
