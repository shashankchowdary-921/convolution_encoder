import streamlit as st


def render_control_panel():
    st.subheader("Simulation Controls")

    input_text = st.text_input(
        "Input Message",
        value="Hello World"
    )

    snr_db = st.slider(
        "Signal-to-Noise Ratio (dB)",
        0.0, 15.0, 5.0, 0.5
    )

    code_rate = st.radio(
        "Code Rate",
        options=["1/2", "2/3"],
        horizontal=True,
        help="Rate 1/2: full redundancy. Rate 2/3: punctured — higher throughput, lower error protection."
    )

    col1, col2 = st.columns(2)
    with col1:
        show_trellis = st.checkbox("Show Trellis Diagram", value=True)
    with col2:
        show_ber = st.checkbox("Show BER Analysis", value=True)

    st.divider()

    return input_text, snr_db, code_rate, show_trellis, show_ber
