import streamlit as st

def render_section_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div style="margin-bottom:20px;">
            <h2 style="
                margin:0;
                color:#111827;
                font-size:1.8rem;
                font-weight:700;
            ">
                {title}
            </h2>

            <p style="
                margin-top:6px;
                color:#6B7280;
                font-size:0.95rem;
            ">
                {subtitle}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
