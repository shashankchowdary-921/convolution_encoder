import streamlit as st


def render_metrics(
    ber,
    errors_corrected,
    recovered_text,
    snr_db
):

    st.write("METRICS FILE LOADED")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("BER", f"{ber:.6f}")

    with c2:
        st.metric("Errors Corrected", errors_corrected)

    with c3:
        st.metric("Recovered Text", recovered_text)

    with c4:
        st.metric("SNR", f"{snr_db:.1f} dB")
