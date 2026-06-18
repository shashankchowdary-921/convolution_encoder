import streamlit as st
import numpy as np
import math

from core.encoder import ConvolutionalEncoder
from core.decoder import ViterbiDecoder
from core.channel import AWGNChannel
from core.utils import text_to_bits, bits_to_text, calculate_ber
from core import ui

# ============================================================================
# Page config
# ============================================================================
st.set_page_config(
    page_title="Conv. Encoder & Viterbi Decoder",
    page_icon="⟨⟩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply global styles — must be first st call after set_page_config
ui.apply_custom_css()

# ============================================================================
# Cached resources
# ============================================================================
@st.cache_resource
def get_encoder():  return ConvolutionalEncoder()
@st.cache_resource
def get_decoder():  return ViterbiDecoder()
@st.cache_resource
def get_channel():  return AWGNChannel()

encoder = get_encoder()
decoder = get_decoder()
channel = get_channel()

# ============================================================================
# Sidebar — returns controls
# ============================================================================
input_text, snr_db, show_trellis, show_ber_plot = ui.render_sidebar()

# ============================================================================
# Header + pipeline rail
# ============================================================================
ui.render_header()

# ============================================================================
# STEP 1 — Text → Binary
# ============================================================================
ui.render_pipeline_rail(active_step=1)
ui.render_section(1, "Text → Binary", "Convert each character to its 8-bit ASCII representation")

binary = text_to_bits(input_text)

col1, col2 = st.columns([1, 3])
with col1:
    st.markdown(f"**Original text**")
    st.code(input_text, language="text")
with col2:
    ui.render_bits(binary, label="8-bit ASCII bitstream")
    ui.render_bit_legend()
    ui.render_metrics([
        {"value": str(len(input_text)), "label": "Characters",    "color_class": "primary"},
        {"value": str(len(binary)),     "label": "Total bits",     "color_class": "primary"},
        {"value": "8",                  "label": "Bits/char"},
    ])

# ============================================================================
# STEP 2 — Convolutional Encoding
# ============================================================================
ui.render_pipeline_rail(active_step=2)
ui.render_section(2, "Convolutional Encoding", "Rate-1/2 encoder with K=3 — each input bit produces 2 output bits")

with st.spinner("Encoding…"):
    encoded = encoder.encode(binary)

ui.render_metrics([
    {"value": "1/2",              "label": "Code rate"},
    {"value": "K = 3",            "label": "Constraint length"},
    {"value": "G₁=111, G₂=101",  "label": "Generators",   "color_class": "primary", "mono": True},
    {"value": str(len(encoded)),  "label": "Encoded bits",  "color_class": "primary"},
])

ui.render_bits(encoded, label="Encoded bitstream")
ui.render_bit_legend()
st.caption(f"Rate-1/2 expansion: {len(binary)} → {len(encoded)} bits")

# ============================================================================
# STEP 3 — AWGN Channel
# ============================================================================
ui.render_pipeline_rail(active_step=3)
ui.render_section(3, "AWGN Channel", f"Adding white Gaussian noise at SNR = {snr_db:.1f} dB")

with st.spinner(f"Transmitting through channel…"):
    received, tx_symbols, rx_symbols = channel.transmit(encoded, snr_db)

flipped_indices = [i for i, (a, b) in enumerate(zip(encoded, received)) if a != b]
n_errors   = len(flipped_indices)
error_rate = n_errors / len(encoded) if encoded else 0

err_color = "success" if n_errors == 0 else ("warning" if error_rate < 0.05 else "danger")

ui.render_metrics([
    {"value": f"{snr_db:.1f} dB", "label": "SNR"},
    {"value": str(n_errors),      "label": "Bits flipped",       "color_class": err_color},
    {"value": f"{error_rate:.2%}","label": "Channel error rate", "color_class": err_color},
    {"value": str(len(encoded)),  "label": "Bits transmitted"},
])

ui.render_bits(received, label="Received (noisy) bitstream", flipped=flipped_indices)
ui.render_bit_legend(show_flipped=True)

# ============================================================================
# STEP 4 — Viterbi Decoding
# ============================================================================
ui.render_pipeline_rail(active_step=4)
ui.render_section(4, "Viterbi Decoding", "Maximum-likelihood sequence estimation over the trellis")

decoded      = ""
decoded_result = None

with st.spinner("Decoding…"):
    try:
        decoded_result = decoder.decode_with_trellis(received)
        decoded        = decoded_result["output"]
    except Exception as e:
        st.error(f"Decoding error: {e}")

if decoded:
    decode_errors = [i for i, (a, b) in enumerate(zip(binary, decoded)) if a != b]
    ui.render_bits(decoded, label="Decoded bitstream", errors=decode_errors)
    ui.render_bit_legend(show_errors=True)
else:
    ui.render_info("Decoding failed — try reducing noise (increase SNR).", "danger")

# ============================================================================
# STEP 5 — Results
# ============================================================================
ui.render_pipeline_rail(active_step=5)
ui.render_section(5, "Results", "Recovered message and error statistics")

recovered_text = bits_to_text(decoded) if decoded else "(failed)"
ber            = calculate_ber(binary, decoded) if binary and decoded else 1.0
is_perfect     = (recovered_text == input_text)

ber_class  = "success" if ber == 0 else ("warning" if ber < 0.01 else "danger")
text_class = "success" if is_perfect else "danger"
status_txt = "Perfect recovery" if is_perfect else "Errors remain"

ui.render_metrics([
    {"value": recovered_text,       "label": "Recovered text",   "color_class": text_class, "mono": True},
    {"value": f"{ber:.6f}",         "label": "Bit error rate",   "color_class": ber_class,  "mono": True},
    {"value": status_txt,           "label": "Status",            "color_class": text_class},
])

if is_perfect:
    ui.render_info("The Viterbi decoder fully recovered the original message.", "success")
else:
    n_bit_errors = len(decode_errors) if decoded else "?"
    ui.render_info(
        f"{n_bit_errors} bit error(s) remain after decoding — try raising the SNR slider.",
        "warning"
    )

# ============================================================================
# TRELLIS DIAGRAM (optional)
# ============================================================================
if show_trellis and decoded_result:
    st.markdown("---")
    ui.render_section("★", "Trellis Diagram", "The maximum-likelihood path found by Viterbi")
    ui.render_trellis(decoded_result.get("trellis_path", []))

# ============================================================================
# BER ANALYSIS (optional)
# ============================================================================
if show_ber_plot:
    st.markdown("---")
    ui.render_section("★", "BER vs SNR Analysis", "Simulated performance vs uncoded BPSK")

    with st.spinner("Running BER sweep (this takes a moment)…"):
        snr_sweep   = np.arange(0, 11, 0.5)
        ber_sweep   = []
        prog        = st.progress(0)
        for idx, snr in enumerate(snr_sweep):
            rx, _, _ = channel.transmit(encoded, snr)
            try:
                dec = decoder.decode(rx)
                ber_sweep.append(calculate_ber(binary, dec))
            except Exception:
                ber_sweep.append(1.0)
            prog.progress((idx + 1) / len(snr_sweep))
        prog.empty()

        def q_fn(x):
            return 0.5 * (1 - math.erf(x / np.sqrt(2)))

        theoretical = [q_fn(np.sqrt(10 ** (s / 10))) for s in snr_sweep]

    ui.render_ber_plot(snr_sweep, ber_sweep, theoretical)

    with st.expander("📋 BER Data Table"):
        ui.render_ber_table(snr_sweep, ber_sweep, theoretical)
