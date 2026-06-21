import streamlit as st

def render_section_header(title, subtitle=""):

    st.subheader(title)

    if subtitle:
        st.caption(subtitle)
