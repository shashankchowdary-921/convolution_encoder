
import streamlit as st


def render_header():

    st.markdown(
        """
        <div style="
            padding-top:10px;
            padding-bottom:20px;
        ">
            <h1 style="
                margin-bottom:4px;
                font-size:2.5rem;
                font-weight:700;
                color:#111111;
            ">
                Convolutional Encoder & Viterbi Decoder
            </h1>

            <p style="
                color:#666666;
                font-size:1rem;
                margin-top:0px;
            ">
                Forward Error Correction Laboratory
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
