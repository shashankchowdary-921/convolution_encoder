import streamlit as st

def render_metric_box(title, value, accent=False):
    value_class = "metric-value-accent" if accent else "metric-value"
    st.markdown(
        f'''
        <div class="pipeline-stage">
            <div class="metric-title">{title}</div>
            <div class="{value_class}" style="margin-top:6px;">{value}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

def render_transmission_section(
    input_text,
    recovered_text,
    ber,
    errors_introduced,
    errors_corrected,
    recovery_efficiency
):
    st.subheader("Transmission Result")

    col1, col2 = st.columns(2)
    with col1:
        render_metric_box("Input Message", input_text)
    with col2:
        render_metric_box("Recovered Message", recovered_text)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_box("BER", f"{ber:.6f}")
    with c2:
        render_metric_box("Errors Introduced", errors_introduced)
    with c3:
        render_metric_box("Errors Corrected", errors_corrected)
    with c4:
        render_metric_box(
            "Recovery Efficiency",
            f"{recovery_efficiency:.1f}%",
            accent=True
        )
