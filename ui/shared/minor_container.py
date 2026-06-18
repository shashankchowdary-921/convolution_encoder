import streamlit as st

def render_minor_container(title, value):

    st.markdown(
        f"""
        <div style="
            border:1px solid #E7E5E4;
            border-radius:14px;
            padding:18px;
            background:#FFFFFF;
            height:120px;
        ">

            <div style="
                color:#6B7280;
                font-size:0.9rem;
                margin-bottom:10px;
            ">
                {title}
            </div>

            <div style="
                color:#111827;
                font-size:1.5rem;
                font-weight:600;
            ">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
