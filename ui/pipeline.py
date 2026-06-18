import streamlit as st


def render_pipeline(stage):

    st.markdown("### Communication Pipeline")

    cols = st.columns(6)

    steps = [
        ("Input", stage["text"]),
        ("Binary", stage["binary"]),
        ("Encoder", stage["encoded"]),
        ("AWGN", f'{stage["snr"]} dB'),
        ("Decoder", stage["decoded"]),
        ("Output", stage["recovered"])
    ]

    for col, (title, value) in zip(cols, steps):

        with col:

            st.markdown(
                f"""
                <div style="
                    background:white;
                    border:1px solid #E5E7EB;
                    border-radius:12px;
                    padding:16px;
                    min-height:120px;
                    display:flex;
                    flex-direction:column;
                    justify-content:space-between;
                ">

                    <div style="
                        font-size:0.75rem;
                        font-weight:600;
                        color:#6B7280;
                        text-transform:uppercase;
                        letter-spacing:0.05em;
                    ">
                        {title}
                    </div>

                    <div style="
                        margin-top:12px;
                        font-size:1rem;
                        font-weight:600;
                        color:#111827;
                        word-break:break-word;
                    ">
                        {value}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )
