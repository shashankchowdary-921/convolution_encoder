import streamlit as st


def render_header():
    st.markdown(
        '<div style="padding:2.5rem 0 1.5rem 0;border-bottom:1px solid #E2E8F0;margin-bottom:1.5rem;">'
        '<h1 style="font-size:2.2rem;font-weight:700;color:#0F172A;margin:0 0 0.5rem 0;line-height:1.2;">Convolutional Encoder <span style="color:#4F46E5">&amp;</span> Viterbi Decoder</h1>'
        '<p style="font-size:1rem;color:#64748B;margin:0 0 1.2rem 0;max-width:680px;line-height:1.6;">End-to-end simulation of forward error correction — encode text through a rate&#8209;1/2 K=3 convolutional encoder, corrupt via AWGN, and recover using Viterbi decoding.</p>'
        '<div style="display:flex;gap:1.5rem;flex-wrap:wrap;">'
        '<div style="font-size:0.82rem;color:#475569;"><span style="color:#4F46E5;font-weight:600;">Rate</span> &nbsp;1/2</div>'
        '<div style="font-size:0.82rem;color:#475569;"><span style="color:#4F46E5;font-weight:600;">Constraint Length</span> &nbsp;K = 3</div>'
        '<div style="font-size:0.82rem;color:#475569;"><span style="color:#4F46E5;font-weight:600;">Generator</span> &nbsp;G1=111 · G2=101</div>'
        '<div style="font-size:0.82rem;color:#475569;"><span style="color:#4F46E5;font-weight:600;">Decoder</span> &nbsp;Viterbi (Hard Decision)</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )
