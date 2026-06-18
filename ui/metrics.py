import streamlit as st


def render_metrics(
    ber,
    errors_corrected,
    recovered_text,
    snr_db
):

    st.markdown("### Results Summary")

    c1, c2, c3, c4 = st.columns(4)

    metrics = [
        ("BER", f"{ber:.6f}"),
        ("Errors Corrected", str(errors_corrected)),
        ("Recovered Text", recovered_text),
        ("SNR", f"{snr_db:.1f} dB")
    ]

    for col, (title, value) in zip(
        [c1, c2, c3, c4],
        metrics
    ):

        with col:

            st.markdown(
                f"""
                <div style="
                    background:white;
                    border:1px solid #E5E7EB;
                    border-radius:12px;
                    padding:20px;
                    text-align:center;
                    min-height:120px;
                ">

                    <div style="
                        font-size:0.8rem;
                        color:#6B7280;
                        text-transform:uppercase;
                        letter-spacing:0.05em;
                        margin-bottom:10px;
                    ">
                        {title}
                    </div>

                    <div style="
                        font-size:1.5rem;
                        font-weight:700;
                        color:#111827;
                        word-break:break-word;
                    ">
                        {value}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )
