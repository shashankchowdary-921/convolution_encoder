```python
import streamlit as st


def apply_custom_css():

    st.markdown("""
    <style>

    .stApp {
        background-color: #F8F7F4;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1,h2,h3,h4,h5,h6 {
        color: #111111;
        font-weight: 600;
    }

    p, span, div {
        color: #333333;
    }

    .card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px;
    }

    .metric-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }

    .metric-title {
        color: #6B7280;
        font-size: 0.85rem;
    }

    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #111111;
    }

    </style>
    """, unsafe_allow_html=True)
```
