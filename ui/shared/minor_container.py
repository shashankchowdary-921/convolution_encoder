import streamlit as st

def render_minor_container(title, value):

    st.metric(
        label=title,
        value=value
    )
