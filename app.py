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

from ui import (
apply_custom_css,
render_header,
render_control_panel,
render_pipeline,
render_metrics,
render_bitstream,
render_bit_comparison,
render_trellis,
render_ber_plot
)

# =====================================================

# PAGE CONFIG

# =====================================================

st.set_page_config(
page_title="Convolutional Encoder & Viterbi Decoder",
page_icon="📡",
layout="wide"
)

apply_custom_css()

# =====================================================

# CACHE OBJECTS

# =====================================================
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
# =====================================================

# HEADER

# =====================================================

render_header()

# =====================================================

# CONTROLS

# =====================================================
(
    input_text,
    snr_db,
    run_clicked,
    show_trellis,
    show_ber
) = render_control_panel()

if not run_clicked:
    st.info("Enter a message and click Run Simulation.")
    st.stop()

# =====================================================
# PROCESSING
# =====================================================

binary = text_to_bits(input_text)

encoded = encoder.encode(binary)

received, tx_symbols, rx_symbols = channel.transmit(
    encoded,
    snr_db
)

channel_errors = sum(
    1
    for a, b in zip(encoded, received)
    if a != b
)

decoded_result = decoder.decode_with_trellis(received)

decoded = decoded_result["output"]

recovered_text = bits_to_text(decoded)

ber = calculate_ber(
    binary,
    decoded
)

remaining_errors = sum(
    1
    for a, b in zip(binary, decoded)
    if a != b
)

errors_corrected = max(
    channel_errors - remaining_errors,
    0
)
# =====================================================

# PIPELINE DATA

# =====================================================

stage = {
"text": input_text,
"binary": f"{len(binary)} bits",
"encoded": f"{len(encoded)} bits",
"snr": round(snr_db, 1),
"decoded": f"{len(decoded)} bits",
"recovered": recovered_text
}

# =====================================================

# PIPELINE

# =====================================================

render_pipeline(stage)

# =====================================================

# KPI CARDS

# =====================================================

render_metrics(
ber,
errors_corrected,
recovered_text,
snr_db
)

st.markdown("---")

# =====================================================

# TABS

# =====================================================

st.markdown("---")
st.header("Overview")

# overview content

st.markdown("---")
st.header("Bitstream Analysis")

# bit comparison

st.markdown("---")
st.header("Trellis Diagram")

# trellis

st.markdown("---")
st.header("BER Performance")

# ber plot

# =====================================================

# OVERVIEW

# =====================================================
# =====================================================
# OVERVIEW
# =====================================================
st.markdown("---")
st.header("Overview")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Input")

    st.write(input_text)

    st.metric(
        "Input Bits",
        len(binary)
    )

    st.metric(
        "Encoded Bits",
        len(encoded)
    )

with col2:

    st.subheader("Output")

    st.write(recovered_text)

    st.metric(
        "Channel Errors",
        channel_errors
    )

    st.metric(
        "Remaining Errors",
        remaining_errors
    )
# =====================================================

# BIT ANALYSIS

# =====================================================

# =====================================================
# BIT ANALYSIS
# =====================================================

st.markdown("---")
st.header("Bitstream Analysis")

render_bit_comparison(
    binary,
    received,
    decoded
)

# =====================================================

# TRELLIS
# =====================================================
# TRELLIS
# =====================================================

st.markdown("---")
st.header("Trellis Diagram")

if show_trellis:

    render_trellis(
        decoded_result["trellis_path"]
    )

else:

    st.info(
        "Enable Trellis Diagram in controls."
    )
# =====================================================
# BER ANALYSIS
# =====================================================

st.markdown("---")
st.header("BER Performance Analysis")

if show_ber:

    with st.spinner(
        "Running BER analysis..."
    ):

            snr_values = np.arange(
                0,
                11,
                0.5
            )

            ber_values = []

            progress = st.progress(0)

            for idx, snr in enumerate(
                snr_values
            ):

                rx_bits, _, _ = channel.transmit(
                    encoded,
                    snr
                )

                decoded_bits = decoder.decode(
                    rx_bits
                )

                ber_values.append(
                    calculate_ber(
                        binary,
                        decoded_bits
                    )
                )

                progress.progress(
                    (idx + 1)
                    / len(snr_values)
                )

            progress.empty()

            def q_function(x):

                return 0.5 * (
                    1 -
                    math.erf(
                        x / np.sqrt(2)
                    )
                )

            theoretical_ber = [

                q_function(
                    np.sqrt(
                        10 ** (snr / 10)
                    )
                )

                for snr in snr_values
            ]

            render_ber_plot(
                snr_values,
                ber_values,
                theoretical_ber
            )

    else:

        st.info(
            "Enable BER Analysis in controls."
        )
