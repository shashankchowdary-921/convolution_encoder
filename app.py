"""
app.py – Clean, professional Streamlit application
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
    render_pipeline,
    render_summary,
    render_bitstream,
    render_trellis,
    render_ber_plot,
    render_overview_tab,
    render_bit_analysis
)

st.set_page_config(
    page_title="Convolutional Encoder & Viterbi Decoder",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_css()

# ─── Session state for simulation results ──────────────────────────────

if 'results' not in st.session_state:
    st.session_state.results = {}

# ─── Sidebar ─────────────────────────────────────────────────────────────

input_text, snr_db, run_clicked, show_trellis, show_ber = render_sidebar()

# ─── Main header ────────────────────────────────────────────────────────

render_header()

# ─── Run simulation only when button is pressed ────────────────────────

if run_clicked:
    # Encode
    binary = text_to_bits(input_text)
    encoder = ConvolutionalEncoder()
    encoded = encoder.encode(binary)

    # Channel
    channel = AWGNChannel()
    received, _, _ = channel.transmit(encoded, snr_db)

    # Decode
    decoder = ViterbiDecoder()
    decoded_result = decoder.decode_with_trellis(received)
    decoded = decoded_result['output']
    recovered_text = bits_to_text(decoded) if decoded else "(decoding failed)"

    # BER
    ber = calculate_ber(binary, decoded) if binary and decoded else 1.0
    flipped_indices = [i for i, (a,b) in enumerate(zip(encoded, received)) if a != b]
    error_indices = [i for i, (a,b) in enumerate(zip(binary, decoded)) if a != b]
    errors_corrected = len(error_indices)

    # Store
    st.session_state.results = {
        'input_text': input_text,
        'binary': binary,
        'encoded': encoded,
        'received': received,
        'decoded': decoded,
        'recovered_text': recovered_text,
        'ber': ber,
        'snr': snr_db,
        'trellis_path': decoded_result['trellis_path'],
        'flipped_indices': flipped_indices,
        'error_indices': error_indices,
        'errors_corrected': errors_corrected
    }

# ─── Display results if available ──────────────────────────────────────

results = st.session_state.results

if results:
    # Pipeline
    stage = {
        "text": results['input_text'],
        "binary": results['binary'][:20] + "…" if len(results['binary'])>20 else results['binary'],
        "encoded": results['encoded'][:20] + "…" if len(results['encoded'])>20 else results['encoded'],
        "snr": results['snr'],
        "decoded": results['decoded'][:20] + "…" if len(results['decoded'])>20 else results['decoded'],
        "recovered": results['recovered_text']
    }
    render_pipeline(stage, snr=results['snr'])

    # Summary cards
    render_summary(
        results['input_text'],
        results['recovered_text'],
        results['ber'],
        results['errors_corrected'],
        results['snr']
    )

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Bit Analysis", "Trellis", "BER Performance"])

    with tab1:
        render_overview_tab(stage)

    with tab2:
        # Show all bits in grouped form
        render_bit_analysis(
            results['binary'],
            results['received'],
            results['decoded'],
            results['flipped_indices'],
            results['error_indices']
        )

    with tab3:
        if show_trellis and results['trellis_path']:
            render_trellis(results['trellis_path'])
        else:
            st.info("Trellis diagram disabled or not available.")

    with tab4:
        if show_ber:
            # Recompute BER for a range of SNRs using the current message
            # This could be cached for performance, but we'll compute on the fly.
            with st.spinner("Computing BER curve..."):
                snr_range = np.arange(0, 12, 0.5)
                ber_vals = []
                # Reuse encoder, decoder, channel
                enc = ConvolutionalEncoder()
                dec = ViterbiDecoder()
                ch = AWGNChannel()
                # Encode once
                bitstream = text_to_bits(results['input_text'])
                codeword = enc.encode(bitstream)
                for snr in snr_range:
                    rx, _, _ = ch.transmit(codeword, snr)
                    try:
                        dec_out = dec.decode(rx)
                        ber_vals.append(calculate_ber(bitstream, dec_out))
                    except:
                        ber_vals.append(1.0)
                # Theoretical
                def q_func(x):
                    return 0.5 * (1 - math.erf(x / math.sqrt(2)))
                theo = [q_func(np.sqrt(10**(snr/10))) for snr in snr_range]
                render_ber_plot(snr_range, ber_vals, theo)
        else:
            st.info("BER plot disabled.")

else:
    st.info("Adjust parameters and click **Run Simulation** to see results.")
    
