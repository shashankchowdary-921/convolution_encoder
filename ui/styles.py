import streamlit as st

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
        border-bottom: 2px solid #4F46E5;
        padding-bottom: 0.5rem;
        margin-top: 2.5rem;
        margin-bottom: 1.25rem;
        display: inline-block;
    }
    h3 {
        font-size: 1.1rem;
        color: #4F46E5;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    /* ===== MAJOR CONTAINER ===== */
    /* Use: st.container(border=False) wrapped in a div with this class,
       OR apply via st.markdown div wrapper around a whole section */
    .major-container {
        background: #FFFFFF;
        border: 1px solid #E5E3DD;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 28px;
        box-shadow: 0 1px 3px rgba(17, 17, 17, 0.04), 0 1px 2px rgba(17, 17, 17, 0.03);
    }

    /* ===== MINOR CONTAINER (nested, inside major) ===== */
    .minor-container {
        background: #FAFAF9;
        border: 1px solid #EDEBE5;
        border-radius: 10px;
        padding: 14px 16px;
    }

    /* ===== NATIVE STREAMLIT BORDERED CONTAINERS ===== */
    /* st.container(border=True) renders as div[data-testid="stVerticalBlockBorderWrapper"] */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border: 1px solid #E5E3DD !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 2px rgba(17, 17, 17, 0.03);
    }

    /* ===== METRIC VALUES ===== */
    .metric-title {
        color: #6B7280;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #111111;
        font-variant-numeric: tabular-nums;
    }
    .metric-value-accent {
        font-size: 1.6rem;
        font-weight: 700;
        color: #4F46E5;
        font-variant-numeric: tabular-nums;
    }

    /* ===== PIPELINE STAGE BLOCKS ===== */
    .pipeline-stage {
        background: #FFFFFF;
        border: 1px solid #E5E3DD;
        border-radius: 10px;
        padding: 14px 12px;
        text-align: center;
    }
    .pipeline-arrow {
        color: #C7C5BE;
        font-size: 1.3rem;
        text-align: center;
        line-height: 1;
    }

    /* ===== CODE / MONOSPACE BLOCKS ===== */
    code, .stCodeBlock, pre {
        background-color: #0E1117 !important;
        border-radius: 8px !important;
    }

    </style>
    """, unsafe_allow_html=True)

/* Fallback selectors for different Streamlit versions */
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stContainer"],
    .stContainer > div:first-child {
        background: #FFFFFF !important;
        border: 1px solid #E5E3DD !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 2px rgba(17, 17, 17, 0.03);
    }
