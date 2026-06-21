import streamlit as st


def render_stage(
    title,
    value
):
    with st.container(border=True):

        st.caption(title)

        st.markdown(
            f"### {value}"
        )
