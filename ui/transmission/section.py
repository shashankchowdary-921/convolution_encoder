import streamlit as st

from ui.shared.section_header import render_section_header
from ui.shared.minor_container import render_minor_container


def render_transmission_section(
    input_text,
    recovered_text,
    ber,
    errors_introduced,
    errors_corrected,
    recovery_efficiency
):

    render_section_header(
        "Transmission Result",
        "End-to-end communication performance"
    )

    col1, col2 = st.columns(2)

    with col1:
        render_minor_container(
            "Input Message",
            input_text
        )

    with col2:
        render_minor_container(
            "Recovered Message",
            recovered_text
        )

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        render_minor_container(
            "BER",
            f"{ber:.6f}"
        )

    with c2:
        render_minor_container(
            "Errors Introduced",
            errors_introduced
        )

    with c3:
        render_minor_container(
            "Errors Corrected",
            errors_corrected
        )

    with c4:
        render_minor_container(
            "Recovery Efficiency",
            f"{recovery_efficiency:.1f}%"
        )
