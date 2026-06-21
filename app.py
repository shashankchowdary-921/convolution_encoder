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

from ui.styles import apply_custom_css

from ui.header import render_header

from ui.control_panel import (
    render_control_panel
)

from ui.metrics import (
    render_metrics
)

from ui.bitstream import (
    render_bitstream,
    render_bit_comparison
)

from ui.trellis import (
    render_trellis
)

from ui.ber import (
    render_ber_plot
)

from ui.pipeline.section import (
    render_pipeline_section
)

from ui.transmission.section import (
    render_transmission_section
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
    show_trellis,
    show_ber
) = render_control_panel()



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

decoded_raw = decoded_result["output"]

st.write(len(binary), len(decoded_raw))

decoded = decoded_raw[:-2]

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
# RECOVERY METRICS
# =====================================================

recovery_efficiency = 100.0

if channel_errors > 0:

    recovery_efficiency = (
        errors_corrected
        /
        channel_errors
    ) * 100
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

render_pipeline_section(stage)

# =====================================================

# KPI CARDS

# =====================================================
# =====================================================
# TRANSMISSION RESULT
# =====================================================

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

# TABS

# =====================================================


# ber plot

# =====================================================

# OVERVIEW

# =====================================================
#============================

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
        ber_test_message = (
            "The quick brown fox jumps over the lazy dog "
            "while engineers debug convolutional codes."
        )
        ber_test_bits = text_to_bits(ber_test_message)
        ber_test_encoded = encoder.encode(ber_test_bits)

        snr_values = np.arange(
            0,
            11,
            0.5
        )
        ber_values = []
        progress = st.progress(0)
        num_trials = 50
        for idx, snr in enumerate(
            snr_values
        ):
            trial_bers = []
            for _ in range(num_trials):
                rx_bits, _, _ = channel.transmit(
                    ber_test_encoded,
                    snr
                )
                decoded_bits = decoder.decode(
                    rx_bits
                )
                decoded_bits = decoded_bits[:-2]
                trial_bers.append(
                    calculate_ber(
                        ber_test_bits,
                        decoded_bits
                    )
                )
            ber_values.append(
                sum(trial_bers) / num_trials
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
