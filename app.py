import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

from core.encoder import ConvolutionalEncoder
from core.decoder import ViterbiDecoder
from core.channel import AWGNChannel
from core.utils import text_to_bits, bits_to_text, calculate_ber

# ============================================================================
# Page Configuration
# ============================================================================
st.set_page_config(
    page_title="Convolutional Encoder & Viterbi Decoder",
    page_icon="🔐",
    layout="wide"
)

# ============================================================================
# Custom CSS
# ============================================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .bit-display {
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        background-color: #f0f2f6;
        padding: 0.75rem;
        border-radius: 0.5rem;
        word-wrap: break-word;
        overflow-x: auto;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# Initialize Components (cached for performance)
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
    st.title("⚙️ Controls")
    
    st.subheader("📝 Input Message")
    input_text = st.text_area(
        "Enter your message:",
        value="Hello World",
        max_chars=200
    )
    
    st.subheader("📡 Channel Settings")
    snr_db = st.slider(
        "Signal-to-Noise Ratio (dB)",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.5
    )
    
    st.subheader("🔧 Advanced Options")
    show_trellis = st.checkbox("Show Trellis Diagram", value=True)
    show_ber_plot = st.checkbox("Show BER vs SNR Plot", value=True)

# ============================================================================
# Main Content
# ============================================================================
st.markdown('<p class="main-header">🔐 Convolutional Encoder & Viterbi Decoder</p>', unsafe_allow_html=True)
st.markdown("*Interactive demonstration of forward error correction for digital communication*")

# -------------------------------------------------------------------------
# Step 1: Text → Binary
# -------------------------------------------------------------------------
st.markdown('<p class="section-header">📝 Step 1: Text → Binary</p>', unsafe_allow_html=True)

binary = text_to_bits(input_text)
st.markdown(f'<div class="bit-display">{binary}</div>', unsafe_allow_html=True)
st.caption(f"Length: {len(binary)} bits ({len(input_text)} characters × 8 bits)")

# -------------------------------------------------------------------------
# Step 2: Convolutional Encoding
# -------------------------------------------------------------------------
st.markdown('<p class="section-header">⚙️ Step 2: Convolutional Encoding</p>', unsafe_allow_html=True)

with st.spinner("Encoding..."):
    encoded = encoder.encode(binary)

st.markdown(f'<div class="bit-display">{encoded}</div>', unsafe_allow_html=True)
st.caption(f"Length: {len(encoded)} bits (Rate 1/2 expansion)")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Code Rate", "1/2")
with col2:
    st.metric("Constraint Length (K)", "3")
with col3:
    st.metric("Generator Polynomials", "G₁=111, G₂=101")

# -------------------------------------------------------------------------
# Step 3: AWGN Channel
# -------------------------------------------------------------------------
st.markdown('<p class="section-header">📡 Step 3: AWGN Channel</p>', unsafe_allow_html=True)

with st.spinner(f"Adding AWGN noise at SNR = {snr_db} dB..."):
    received, tx_symbols, rx_symbols = channel.transmit(encoded, snr_db)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("SNR", f"{snr_db} dB")
with col2:
    errors = sum(1 for a, b in zip(encoded, received) if a != b)
    st.metric("Bits Flipped", f"{errors} / {len(encoded)}")
with col3:
    error_rate = errors / len(encoded) if len(encoded) > 0 else 0
    st.metric("Channel Error Rate", f"{error_rate:.2%}")

st.markdown(f'<div class="bit-display">Received: {received}</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Step 4: Viterbi Decoding
# -------------------------------------------------------------------------
st.markdown('<p class="section-header">🔍 Step 4: Viterbi Decoding</p>', unsafe_allow_html=True)

with st.spinner("Decoding with Viterbi algorithm..."):
    try:
        decoded_result = decoder.decode_with_trellis(received)
        decoded = decoded_result['output']
    except Exception as e:
        st.error(f"Decoding error: {e}")
        decoded = ""

st.markdown(f'<div class="bit-display">{decoded}</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Step 5: Results
# -------------------------------------------------------------------------
st.markdown('<p class="section-header">✅ Step 5: Results</p>', unsafe_allow_html=True)

recovered_text = bits_to_text(decoded) if decoded else "(decoding failed)"
ber = calculate_ber(binary, decoded) if binary and decoded else 1.0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Recovered Text", recovered_text)
with col2:
    st.metric("Bit Error Rate (BER)", f"{ber:.6f}")
with col3:
    if recovered_text == input_text:
        st.success("✅ Perfect Recovery!")
    else:
        st.warning("⚠️ Some errors remain")

# -------------------------------------------------------------------------
# Bonus: Trellis Diagram
# -------------------------------------------------------------------------
if show_trellis and 'decoded_result' in locals() and decoded_result:
    st.markdown('<p class="section-header">🔱 Trellis Diagram</p>', unsafe_allow_html=True)
    
    trellis_path = decoded_result['trellis_path']
    state_labels = ['00', '01', '10', '11']
    
    if trellis_path:
        fig = go.Figure()
        
        # Draw state circles
        num_steps = len(trellis_path) + 1
        for step in range(num_steps):
            for state in range(4):
                fig.add_trace(go.Scatter(
                    x=[step],
                    y=[state],
                    mode='markers',
                    marker=dict(size=12, color='lightgray'),
                    showlegend=False,
                    hoverinfo='text',
                    text=f"Step {step}<br>State {state_labels[state]}"
                ))
        
        # Draw winning path
        path_x, path_y = [], []
        for i, transition in enumerate(trellis_path):
            from_state = transition['from_state']
            to_state = transition['to_state']
            input_bit = transition['input_bit']
            
            path_x.extend([i, i+1, None])
            path_y.extend([from_state, to_state, None])
            
            fig.add_annotation(
                x=(i + i+1) / 2,
                y=(from_state + to_state) / 2 + 0.2,
                text=f"b={input_bit}",
                showarrow=False,
                font=dict(size=10, color='blue')
            )
        
        fig.add_trace(go.Scatter(
            x=path_x,
            y=path_y,
            mode='lines+markers',
            line=dict(color='red', width=3),
            marker=dict(size=10, color='red'),
            name='Winning Path'
        ))
        
        fig.update_layout(
            title="Viterbi Decoder Trellis Path",
            xaxis_title="Time Step",
            yaxis_title="State",
            yaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3],
                ticktext=state_labels
            ),
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------------------
# Bonus: BER vs SNR Plot
# -------------------------------------------------------------------------
if show_ber_plot:
    st.markdown('<p class="section-header">📊 BER Performance</p>', unsafe_allow_html=True)
    
    with st.spinner("Running BER analysis..."):
        snr_values = np.arange(0, 11, 0.5)
        ber_values = []
        
        for snr in snr_values:
            rx, _, _ = channel.transmit(encoded, snr)
            try:
                dec = decoder.decode(rx)
                ber_values.append(calculate_ber(binary, dec))
            except:
                ber_values.append(1.0)
        
        def q_function(x):
            return 0.5 * (1 - np.math.erf(x / np.sqrt(2)))
        
        theoretical_ber = [q_function(np.sqrt(10 ** (snr/10))) for snr in snr_values]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.semilogy(snr_values, ber_values, 'bo-', label='Simulated (Viterbi Decoded)', markersize=8)
        ax.semilogy(snr_values, theoretical_ber, 'r--', label='Theoretical (Uncoded BPSK)', linewidth=2)
        ax.set_xlabel('SNR (dB)')
        ax.set_ylabel('Bit Error Rate (BER)')
        ax.set_title('BER vs SNR for Convolutional Code (Rate 1/2, K=3)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_ylim([1e-6, 1])
        
        st.pyplot(fig)
        plt.close(fig)
