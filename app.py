import streamlit as st
import numpy as np
import math

from core.encoder import ConvolutionalEncoder
from core.decoder import ViterbiDecoder
from core.channel import AWGNChannel
from core.utils import (
    text_to_bits,
    bits_to_text,
    calculate_ber
)

from ui.ber import (
    render_ber_plot,
    render_constellation_plot
)

from ui.styles import apply_custom_css
from ui.header import render_header
from ui.control_panel import render_control_panel
from ui.bitstream import render_bitstream, render_bit_comparison
from ui.trellis import render_trellis
from ui.pipeline.section import render_pipeline_section
from ui.transmission.section import render_transmission_section

st.set_page_config(
    page_title="Convolutional Encoder & Viterbi Decoder",
    page_icon="📡",
    layout="wide"
)

apply_custom_css()


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

render_header()

input_text, snr_db, code_rate, show_trellis, show_ber = render_control_panel()

# =====================================================
# PROCESSING
# =====================================================
binary = text_to_bits(input_text)

if code_rate == "2/3":
    encoded = encoder.encode_punctured(binary)
else:
    encoded = encoder.encode(binary)

received, tx_symbols, rx_symbols = channel.transmit(encoded, snr_db)

channel_errors = sum(1 for a, b in zip(encoded, received) if a != b)

if code_rate == "2/3":
    decoded_result = decoder.decode_punctured_with_trellis(received)
else:
    decoded_result = decoder.decode_with_trellis(received)

decoded_raw = decoded_result["output"]
decoded = decoded_raw[:-2]

recovered_text = bits_to_text(decoded)
ber = calculate_ber(binary, decoded)

remaining_errors = sum(1 for a, b in zip(binary, decoded) if a != b)
errors_corrected = max(channel_errors - remaining_errors, 0)

recovery_efficiency = 100.0
if channel_errors > 0:
    recovery_efficiency = (errors_corrected / channel_errors) * 100

# =====================================================
# PIPELINE
# =====================================================
stage = {
    "text": input_text,
    "binary": f"{len(binary)} bits",
    "encoded": f"{len(encoded)} bits",
    "snr": round(snr_db, 1),
    "decoded": f"{len(decoded)} bits",
    "recovered": recovered_text
}

render_pipeline_section(stage)

render_transmission_section(
    input_text=input_text,
    recovered_text=recovered_text,
    ber=ber,
    errors_introduced=channel_errors,
    errors_corrected=errors_corrected,
    recovery_efficiency=recovery_efficiency
)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# BITSTREAM
# =====================================================
st.markdown("---")
st.header("Bitstream Analysis")
render_bit_comparison(binary, received, decoded)

# =====================================================
# TRELLIS
# =====================================================
st.markdown("---")
st.header("Trellis Diagram")
if show_trellis:
    render_trellis(decoded_result["trellis_path"])
else:
    st.info("Enable Trellis Diagram in controls.")

# =====================================================
# BER
# =====================================================
st.markdown("---")
st.header("BER Performance Analysis")

if show_ber:
    with st.spinner("Running BER analysis..."):
        ber_test_message = (
            "The quick brown fox jumps over the lazy dog "
            "while engineers debug convolutional codes."
        )
        ber_test_bits = text_to_bits(ber_test_message)

        if code_rate == "2/3":
            ber_test_encoded = encoder.encode_punctured(ber_test_bits)
        else:
            ber_test_encoded = encoder.encode(ber_test_bits)

        snr_values = np.arange(0, 11, 0.5)
        ber_values = []
        progress = st.progress(0)
        num_trials = 50

        for idx, snr in enumerate(snr_values):
            trial_bers = []
            for _ in range(num_trials):
                rx, _, _ = channel.transmit(ber_test_encoded, snr)
                if code_rate == "2/3":
                    dec_bits = decoder.decode_punctured(rx)
                else:
                    dec_bits = decoder.decode(rx)
                dec_bits = dec_bits[:-2]
                trial_bers.append(calculate_ber(ber_test_bits, dec_bits))
            ber_values.append(sum(trial_bers) / num_trials)
            progress.progress((idx + 1) / len(snr_values))

        progress.empty()

        st.markdown("---")
        st.subheader("BPSK Constellation Diagram")
        render_constellation_plot(tx_symbols, rx_symbols, snr_db)

        def q_function(x):
            return 0.5 * (1 - math.erf(x / np.sqrt(2)))

        theoretical_ber = [
            q_function(np.sqrt(10 ** (snr / 10)))
            for snr in snr_values
        ]

        render_ber_plot(
            snr_values,
            ber_values,
            theoretical_ber,
            num_trials=num_trials,
            snr_step=0.5
        )
else:
    st.info("Enable BER Analysis in controls.")
