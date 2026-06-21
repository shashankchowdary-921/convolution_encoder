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

def render_diff_html(reference, target):
    """
    Build an HTML string highlighting bit positions where
    target differs from reference. Grouped in bytes of 8.
    """
    spans = []
    for i, bit in enumerate(target):
        ref_bit = reference[i] if i < len(reference) else None
        mismatch = ref_bit is not None and bit != ref_bit
        if mismatch:
            spans.append(
                f'<span style="color:#ffffff; background:#e0353f; '
                f'padding:1px 3px; border-radius:3px; font-weight:700;">{bit}</span>'
            )
        else:
            spans.append(
                f'<span style="color:#d6def0;">{bit}</span>'
            )
        if (i + 1) % 8 == 0:
            spans.append(" ")
    return "".join(spans)

def render_bit_comparison(original, received, decoded):
    st.subheader("Bitstream Comparison")
    st.caption(
        "Received and Decoded shown against Original — "
        "mismatched bits highlighted in red"
    )
    st.markdown("**Original**")
    st.code(group_bits(original), language="text")
    st.markdown("**Received** (after AWGN channel)")
    st.markdown(
        f'<div style="font-family:monospace; background:#0e1117; '
        f'padding:12px; border-radius:6px; word-break:break-all; '
        f'line-height:1.8;">{render_diff_html(original, received)}</div>',
        unsafe_allow_html=True
    )
    st.markdown("**Decoded** (after Viterbi correction)")
    st.markdown(
        f'<div style="font-family:monospace; background:#0e1117; '
        f'padding:12px; border-radius:6px; word-break:break-all; '
        f'line-height:1.8;">{render_diff_html(original, decoded)}</div>',
        unsafe_allow_html=True
    )
