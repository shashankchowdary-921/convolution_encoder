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

def render_arrow():
    st.markdown(
        '<div class="pipeline-arrow">&#8594;</div>',
        unsafe_allow_html=True
    )

def render_pipeline_section(stage):
    st.subheader("Communication Pipeline")
    st.caption(
        "Signal flow through the communication system"
    )

    cols = st.columns([4, 1, 4, 1, 4, 1, 4, 1, 4])

    with cols[0]:
        render_stage("Binary", stage["binary"])
    with cols[1]:
        render_arrow()
    with cols[2]:
        render_stage("Encoder", stage["encoded"])
    with cols[3]:
        render_arrow()
    with cols[4]:
        render_stage("AWGN", f'{stage["snr"]} dB')
    with cols[5]:
        render_arrow()
    with cols[6]:
        render_stage("Decoder", stage["decoded"])
    with cols[7]:
        render_arrow()
    with cols[8]:
        render_stage("Output", stage["recovered"])
