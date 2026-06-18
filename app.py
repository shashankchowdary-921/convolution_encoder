"""
app.py - Main Streamlit Application
Premium UI with real-time updates
"""

import streamlit as st
import numpy as np
import math

# Core logic
from core.encoder import ConvolutionalEncoder
from core.decoder import ViterbiDecoder
from core.channel import AWGNChannel
from core.utils import text_to_bits, bits_to_text, calculate_ber

# Premium UI components
from core.ui import (
    apply_custom_css,
    render_header,
    render_sidebar,
    render_section,
    close_section,
    render_bits,
    render_metrics,
    render_badge,
    render_info_box,
    render_trellis,
    render_ber_plot,
    render_ber_table,
    render_compare_bits,
    render_status_indicator
)

# ============================================================================
# Page Config
# ============================================================================
st.set_page_config(
    page_title="Convolutional Encoder & Viterbi Decoder",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# Apply Premium Styling
# ============================================================================
apply_custom_css()

# ============================================================================
# Initialize Components (Cached)
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
# Sidebar
# ============================================================================
input_text, snr_db, show_trellis, show_ber_plot = render_sidebar()

# ============================================================================
# Main Content
# ============================================================================
render_header()

# ============================================================================
# STEP 1: Text to Binary (Auto-runs on text change)
# ============================================================================
render_section("Text to Binary", 1, "📝")
binary = text_to_bits(input_text)

st.markdown(f"**Input:** `{input_text}`")
render_bits(binary, label="8-bit ASCII Binary")
close_section()

# ============================================================================
# STEP 2: Convolutional Encoding (Auto-runs on binary change)
# ============================================================================
render_section("Convolutional Encoding", 2, "⚙️")
encoded = encoder.encode(binary)

# Metrics
render_metrics([
    {"value": "1/2", "label": "Code Rate", "color_class": "primary"},
    {"value": "K=3", "label": "Constraint Length", "color_class": "primary"},
    {"value": "G₁=111, G₂=101", "label": "Generator Polynomials", "color_class": "primary"},
    {"value": len(encoded), "label": "Encoded Bits", "color_class": "primary"},
])

render_bits(encoded, label="Encoded Bitstream")
close_section()

# ============================================================================
# STEP 3: AWGN Channel (Auto-runs on SNR change)
# ============================================================================
render_section("AWGN Channel", 3, "📡")
received, tx_symbols, rx_symbols = channel.transmit(encoded, snr_db)

# Count errors
errors = sum(1 for a, b in zip(encoded, received) if a != b)
error_rate = errors / len(encoded) if len(encoded) > 0 else 0

render_metrics([
    {"value": f"{snr_db:.1f} dB", "label": "SNR", "color_class": "primary"},
    {"value": errors, "label": "Bits Flipped", "color_class": "danger" if errors > 0 else "success"},
    {"value": f"{error_rate:.2%}", "label": "Channel Error Rate", "color_class": "danger" if error_rate > 0.01 else "success"},
    {"value": len(encoded), "label": "Total Bits", "color_class": "primary"},
])

# Find flipped indices
flipped_indices = [i for i, (a, b) in enumerate(zip(encoded, received)) if a != b]

render_bits(received, label="Received (Noisy)", highlight_flipped=flipped_indices)
close_section()

# ============================================================================
# STEP 4: Viterbi Decoding (Auto-runs on received change)
# ============================================================================
render_section("Viterbi Decoding", 4, "🔍")
try:
    decoded_result = decoder.decode_with_trellis(received)
    decoded = decoded_result['output']
except Exception as e:
    st.error(f"Decoding error: {e}")
    decoded = ""

render_bits(decoded, label="Decoded Bitstream")
close_section()

# ============================================================================
# STEP 5: Results (Auto-runs on decoded change)
# ============================================================================
render_section("Results", 5, "✅")

recovered_text = bits_to_text(decoded) if decoded else "(decoding failed)"
ber = calculate_ber(binary, decoded) if binary and decoded else 1.0
is_perfect = recovered_text == input_text

# Metrics
error_indices = [i for i, (a, b) in enumerate(zip(binary, decoded)) if a != b]
render_metrics([
    {"value": recovered_text, "label": "Recovered Text", "color_class": "success" if is_perfect else "warning"},
    {"value": f"{ber:.6f}", "label": "Bit Error Rate (BER)", "color_class": "success" if ber == 0 else "warning"},
    {"value": f"{len(error_indices)}", "label": "Errors Remaining", "color_class": "success" if ber == 0 else "danger"},
])

# Status indicator
render_status_indicator(snr_db, ber, is_perfect)

# Side-by-side comparison
st.markdown("#### 📊 Bitstream Comparison")
render_compare_bits(binary, received, decoded, flipped_indices)
close_section()

# ============================================================================
# TRELLIS DIAGRAM (Auto-runs on decoded_result change)
# ============================================================================
if show_trellis and 'decoded_result' in locals() and decoded_result:
    render_section("Trellis Diagram", "🔱", "🔱")
    render_trellis(decoded_result['trellis_path'])
    close_section()

# ============================================================================
# BER PERFORMANCE (Auto-runs on show_ber_plot change)
# ============================================================================
if show_ber_plot:
    render_section("BER Performance Analysis", "📊", "📊")
    
    with st.spinner("Running BER analysis..."):
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
        
        render_ber_plot(snr_values, ber_values, theoretical_ber)
        
        with st.expander("📋 View Data Table"):
            render_ber_table(snr_values, ber_values, theoretical_ber)
    
    close_section()
