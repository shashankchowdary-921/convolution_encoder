import streamlit as st

from ui.pipeline.stage import render_stage


def render_pipeline_section(stage):

    st.subheader(
        "Communication Pipeline"
    )

    cols = st.columns(
        [2,1,2,1,2,1,2,1,2]
    )

    with cols[0]:
        render_stage(
            "Binary",
            stage["binary"]
        )

    with cols[1]:
        st.markdown(
            "<h2 style='text-align:center;'>→</h2>",
            unsafe_allow_html=True
        )

    with cols[2]:
        render_stage(
            "Encoder",
            stage["encoded"]
        )

    with cols[3]:
        st.markdown(
            "<h2 style='text-align:center;'>→</h2>",
            unsafe_allow_html=True
        )

    with cols[4]:
        render_stage(
            "AWGN",
            f'{stage["snr"]} dB'
        )

    with cols[5]:
        st.markdown(
            "<h2 style='text-align:center;'>→</h2>",
            unsafe_allow_html=True
        )

    with cols[6]:
        render_stage(
            "Decoder",
            stage["decoded"]
        )

    with cols[7]:
        st.markdown(
            "<h2 style='text-align:center;'>→</h2>",
            unsafe_allow_html=True
        )

    with cols[8]:
        render_stage(
            "Output",
            stage["recovered"][:10]
        )
