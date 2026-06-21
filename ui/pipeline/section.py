import streamlit as st

from ui.pipeline.stage import render_stage


def render_pipeline_section(stage):

    st.subheader("Communication Pipeline")

    st.caption(
        "Signal flow through the communication system"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        render_stage(
            "Binary",
            stage["binary"]
        )

    with c2:
        render_stage(
            "Encoder",
            stage["encoded"]
        )

    with c3:
        render_stage(
            "AWGN",
            f'{stage["snr"]} dB'
        )

    with c4:
        render_stage(
            "Decoder",
            stage["decoded"]
        )

    with c5:
        render_stage(
            "Output",
            stage["recovered"][:10]
        )
