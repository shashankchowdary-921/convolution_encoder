import streamlit as st


def render_header():

    st.title("Convolutional Encoder & Viterbi Decoder")

    st.caption(
        "Interactive demonstration of convolutional encoding, transmission through an AWGN channel, and Viterbi decoding for forward error correction in digital communication systems."
    )

    st.divider()
