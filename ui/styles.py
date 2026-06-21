import streamlit as st


def render_stage(title, value):
    st.markdown(
        f'''
        <div class="pipeline-stage">
            <div class="metric-title">{title}</div>
            <div class="metric-value" style="margin-top:6px;">{value}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )


def apply_custom_css():
    st.markdown("""
    <style>
    /* ===== BASE ===== */
    .stApp {
        background-color: #EEECE7;
    }
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #111111;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    p, span, label {
        color: #374151;
    }
    /* ===== SECTION HEADERS ===== */
    h2 {
        font-size: 1.5rem;
