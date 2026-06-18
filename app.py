"""
app.py - Main Streamlit Application
Uses the revamped UI module.
"""

import streamlit as st
import numpy as np
import math

from core.encoder import ConvolutionalEncoder
from core.decoder import ViterbiDecoder
from core.channel import AWGNChannel
from core.utils import text_to_bits, bits_to_text, calculate_ber

from core.ui import (
    apply_custom_css,
    render_header,
    render_sidebar,
    open_section,
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

st.set_page_config(page_title="ConvEncoder & Viterbi Decoder", page_icon="🔐", layout="wide")
apply_custom_css()

@st.cache_resource
def get_encoder(): return ConvolutionalEncoder()
@st.cache_resource
def get_decoder(): return ViterbiDecoder()
@st.cache_resource
def get_channel(): return AWGNChannel()

encoder, decoder, channel = get_encoder(), get_decoder(), get_channel()
input_text, snr_db, show_trellis, show_ber_plot = render_sidebar()
render_header()

# --- Step 1 ---
open_section("Text to Binary", 1, "📝", "ASCII")
binary = text_to_bits(input_text)
st.markdown(f"**Input:** `{input_text}`")
render_bits(binary, label="8-bit ASCII Binary", icon="🔵")
close_section()

# --- Step 2 ---
open_section("Convolutional Encoding", 2, "⚙️", "Rate 1/2")
encoded = encoder.encode(binary)
render_metrics([
    {"value": "1/2", "label": "Code Rate", "icon": "📊", "color_class": "primary"},
    {"value": "K=3", "label": "Constraint Length", "icon": "🔢", "color_class": "primary"},
    {"value": "G₁=111, G₂=101", "label": "Generator Polynomials", "icon": "🧬", "color_class": "primary"},
    {"value": len(encoded), "label": "Encoded Bits", "icon": "📏", "color_class": "primary"},
])
render_bits(encoded, label="Encoded Bitstream", icon="⚙️")
close_section()

# --- Step 3 ---
open_section("AWGN Channel", 3, "📡", f"SNR: {snr_db:.1f} dB")
received, _, _ = channel.transmit(encoded, snr_db)
errors = sum(1 for a,b in zip(encoded, received) if a!=b)
error_rate = errors / len(encoded) if len(encoded) else 0
render_metrics([
    {"value": f"{snr_db:.1f} dB", "label": "SNR", "icon": "📶", "color_class": "primary"},
    {"value": errors, "label": "Bits Flipped", "icon": "🔄", "color_class": "danger" if errors else "success"},
    {"value": f"{error_rate:.2%}", "label": "Channel Error Rate", "icon": "📉", "color_class": "danger" if error_rate > 0.01 else "success"},
    {"value": len(encoded), "label": "Total Bits", "icon": "📦", "color_class": "primary"},
])
flipped_indices = [i for i,(a,b) in enumerate(zip(encoded, received)) if a!=b]
render_bits(received, label="Received (Noisy)", icon="📡", highlight_flipped=flipped_indices)
close_section()

# --- Step 4 ---
open_section("Viterbi Decoding", 4, "🔍", "MLSE")
try:
    decoded_result = decoder.decode_with_trellis(received)
    decoded = decoded_result['output']
except Exception as e:
    st.error(f"Decoding error: {e}")
    decoded = ""
render_bits(decoded, label="Decoded Bitstream", icon="🔓")
close_section()

# --- Step 5 ---
open_section("Results", 5, "✅", "Summary")
recovered_text = bits_to_text(decoded) if decoded else "(decoding failed)"
ber = calculate_ber(binary, decoded) if binary and decoded else 1.0
is_perfect = recovered_text == input_text
error_indices = [i for i,(a,b) in enumerate(zip(binary, decoded)) if a!=b]
ber_display = f"{ber:.6f}" if ber >= 0.00001 else f"{ber:.2e}"
render_metrics([
    {"value": recovered_text, "label": "Recovered Text", "icon": "📝", "color_class": "success" if is_perfect else "warning"},
    {"value": ber_display, "label": "Bit Error Rate (BER)", "icon": "🎯", "color_class": "success" if ber == 0 else "warning"},
    {"value": f"{len(error_indices)}", "label": "Errors Remaining", "icon": "❌", "color_class": "success" if ber == 0 else "danger"},
])
render_status_indicator(snr_db, ber, is_perfect)
st.markdown("#### 📊 Bitstream Comparison")
render_compare_bits(binary, received, decoded, flipped_indices)
close_section()

# --- Trellis ---
if show_trellis and 'decoded_result' in locals() and decoded_result:
    open_section("Trellis Diagram", "🔱", "🔱", "Viterbi Path")
    render_trellis(decoded_result['trellis_path'])
    close_section()

# --- BER Plot ---
if show_ber_plot:
    open_section("BER Performance Analysis", "📊", "📊", "Analysis")
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
            progress_bar.progress((idx+1)/len(snr_values))
        progress_bar.empty()
        def q_function(x):
            return 0.5 * (1 - math.erf(x / np.sqrt(2)))
        theoretical_ber = [q_function(np.sqrt(10**(snr/10))) for snr in snr_values]
        render_ber_plot(snr_values, ber_values, theoretical_ber)
        with st.expander("📋 View Data Table"):
            render_ber_table(snr_values, ber_values, theoretical_ber)
    close_section()
