```python
import streamlit as st


def render_control_panel():

    st.markdown("### Simulation Controls")

    col1, col2 = st.columns([3, 1])

    with col1:

        input_text = st.text_input(
            "Input Message",
            value="Hello World"
        )

    with col2:

        run_clicked = st.button(
            "Run Simulation",
            use_container_width=True
        )

    st.markdown("")

    snr_db = st.slider(
        "Signal-to-Noise Ratio (dB)",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.5
    )

    col3, col4 = st.columns(2)

    with col3:

        show_trellis = st.checkbox(
            "Show Trellis Diagram",
            value=True
        )

    with col4:

        show_ber = st.checkbox(
            "Show BER Analysis",
            value=True
        )

    st.divider()

    return (
        input_text,
        snr_db,
        run_clicked,
        show_trellis,
        show_ber
    )
```
