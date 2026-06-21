import streamlit as st


def render_stage(title, value):
    st.markdown(
        f'<div class="pipeline-stage">'
        f'<div class="metric-title">{title}</div>'
        f'<div class="metric-value" style="margin-top:6px;">{value}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def apply_custom_css():
    css = (
        "<style>"
        ".stApp { background-color: #EEECE7; }"
        ".block-container { max-width: 1200px; padding-top: 2rem; padding-bottom: 3rem; }"
        "h1, h2, h3, h4, h5, h6 { color: #111111; font-weight: 600; letter-spacing: -0.01em; }"
        "p, span, label { color: #374151; }"
        "h2 { font-size: 1.5rem; border-bottom: 2px solid #4F46E5; padding-bottom: 0.5rem; margin-top: 2.5rem; margin-bottom: 1.25rem; display: inline-block; }"
        "h3 { font-size: 0.8rem; color: #4F46E5; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 700; margin-bottom: 0.5rem; }"
        ".major-container { background: #FFFFFF; border: 1px solid #E5E3DD; border-radius: 16px; padding: 28px 32px; margin-bottom: 28px; box-shadow: 0 1px 3px rgba(17,17,17,0.04), 0 1px 2px rgba(17,17,17,0.03); }"
        ".minor-container { background: #FAFAF9; border: 1px solid #EDEBE5; border-radius: 10px; padding: 14px 16px; }"
        "div[data-testid='stVerticalBlockBorderWrapper'], div[data-testid='stContainer'], .stContainer > div:first-child { background: #FFFFFF !important; border: 1px solid #E5E3DD !important; border-radius: 12px !important; box-shadow: 0 1px 2px rgba(17,17,17,0.03); }"
        ".metric-title { color: #6B7280; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }"
        ".metric-value { font-size: 1.6rem; font-weight: 700; color: #111111; font-variant-numeric: tabular-nums; }"
        ".metric-value-accent { font-size: 1.6rem; font-weight: 700; color: #4F46E5; font-variant-numeric: tabular-nums; }"
        ".pipeline-stage { background: #FFFFFF; border: 1px solid #E5E3DD; border-radius: 10px; padding: 14px 12px; text-align: center; }"
        ".pipeline-arrow { color: #9B9890; font-size: 1.9rem; font-weight: 600; text-align: center; display: flex; align-items: center; justify-content: center; height: 100%; min-height: 88px; }"
        "code, .stCodeBlock, pre { background-color: #0E1117 !important; border-radius: 8px !important; }"
        ".js-plotly-plot .plotly text { fill: #374151 !important; }"
        ".js-plotly-plot .gtitle { fill: #111111 !important; }"
        "</style>"
    )
    st.markdown(css, unsafe_allow_html=True)
