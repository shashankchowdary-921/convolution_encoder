```python
import streamlit as st


def group_bits(bits, group_size=8):

    return " ".join(
        bits[i:i+group_size]
        for i in range(0, len(bits), group_size)
    )


def render_bitstream(bits, title):

    st.subheader(title)

    st.code(
        group_bits(bits),
        language="text"
    )


def render_bit_comparison(
    original,
    received,
    decoded
):

    st.subheader("Bitstream Comparison")

    tab1, tab2, tab3 = st.tabs([
        "Original",
        "Received",
        "Decoded"
    ])

    with tab1:
        st.code(group_bits(original))

    with tab2:
        st.code(group_bits(received))

    with tab3:
        st.code(group_bits(decoded))


