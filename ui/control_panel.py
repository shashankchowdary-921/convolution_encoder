import streamlit as st


def render_control_panel():

    st.markdown(
        """
        <div style="
            margin-bottom:24px;
        ">
            <h3 style="
                margin-bottom:8px;
                color:#111827;
            ">
                Simulation Controls
            </h3>

            <p style="
                color:#6B7280;
                margin-top:0;
            ">
                Configure channel conditions and run the communication chain.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([5, 2])

    with col1:

        input_text = st.text_input(
            "Input Message",
            value="Hello World",
            help="Enter the text message to transmit."
        )

    with col2:

        st.markdown("<br>", unsafe_allow_html=True)

        run_clicked = st.button(
            "Run Simulation",
            use_container_width=True,
            type="primary"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    snr_db = st.slider(
        "Signal-to-Noise Ratio (dB)",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.5
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:

        show_trellis = st.checkbox(
            "Show Trellis Diagram",
            value=True
        )

    with col4:

        show_ber = st.checkbox(
            "Show BER Analysis",
            value=True
        )

    st.markdown(
        """
        <hr style="
            margin-top:20px;
            margin-bottom:30px;
            border:none;
            border-top:1px solid #E5E7EB;
        ">
        """,
        unsafe_allow_html=True
    )

    return (
        input_text,
        snr_db,
        run_clicked,
        show_trellis,
        show_ber
    )
