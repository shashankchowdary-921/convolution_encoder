```python
import streamlit as st


def render_metrics(
    ber,
    errors_corrected,
    recovered_text,
    snr_db
):

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("BER", f"{ber:.6f}"),
        ("Errors Corrected", str(errors_corrected)),
        ("Recovered Text", recovered_text),
        ("SNR", f"{snr_db:.1f} dB")
    ]

    for col, card in zip([c1, c2, c3, c4], cards):

        title, value = card

        with col:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">
                        {title}
                    </div>

                    <div class="metric-value">
                        {value}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
```
