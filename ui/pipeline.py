```python
import streamlit as st


def render_pipeline(stage):

    items = [
        ("Text", stage["text"]),
        ("Binary", stage["binary"]),
        ("Encoder", stage["encoded"]),
        ("AWGN", f'{stage["snr"]} dB'),
        ("Decoder", stage["decoded"]),
        ("Output", stage["recovered"])
    ]

    cols = st.columns(len(items))

    for col, (title, value) in zip(cols, items):

        with col:

            st.markdown(
                f"""
                <div style="
                    background:white;
                    border:1px solid #E5E7EB;
                    border-radius:12px;
                    padding:16px;
                    min-height:120px;
                ">
                    <div style="
                        font-size:0.8rem;
                        color:#666666;
                        margin-bottom:8px;
                    ">
                        {title}
                    </div>

                    <div style="
                        font-weight:600;
                        color:#111111;
                        word-wrap:break-word;
                    ">
                        {value}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
```
