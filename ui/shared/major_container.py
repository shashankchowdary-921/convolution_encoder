import streamlit as st

def open_major_container():

    st.markdown(
        """
        <div style="
            background:white;
            border:1px solid #E7E5E4;
            border-radius:18px;
            padding:28px;
            margin-bottom:24px;
        ">
        """,
        unsafe_allow_html=True
    )

def close_major_container():

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
  
