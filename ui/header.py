import streamlit as st


def render_header():

    st.markdown(
        """
        <div style="
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #E5E7EB;
        ">

            <div style="
                font-size: 2.4rem;
                font-weight: 700;
                color: #111111;
                letter-spacing: -0.03em;
                line-height: 1.1;
                margin-bottom: 0.4rem;
            ">
                Convolutional Encoder & Viterbi Decoder
            </div>

            <div style="
                font-size: 1rem;
                color: #6B7280;
                line-height: 1.6;
                max-width: 800px;
            ">
                Interactive demonstration of convolutional encoding, transmission through an AWGN channel,
                and Viterbi decoding for forward error correction in digital communication systems.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
