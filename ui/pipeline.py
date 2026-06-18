import streamlit as st


def render_pipeline(stage):

    st.write("PIPELINE FILE LOADED")

    cols = st.columns(6)

    cols[0].metric("Input", stage["text"])
    cols[1].metric("Binary", stage["binary"])
    cols[2].metric("Encoder", stage["encoded"])
    cols[3].metric("AWGN", f'{stage["snr"]} dB')
    cols[4].metric("Decoder", stage["decoded"])
    cols[5].metric("Output", stage["recovered"])
