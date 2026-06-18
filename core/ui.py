# core/ui.py

import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# ============================================================
# CSS
# ============================================================

def apply_custom_css():
    st.markdown("""
    <style>

    .stApp {
        background-color: #F8F7F4;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }

    h1,h2,h3,h4 {
        color: #111111;
    }

    .pipeline-container {
        display:flex;
        justify-content:center;
        align-items:center;
        gap:12px;
        flex-wrap:wrap;
        padding:20px;
        margin-bottom:20px;
    }

    .pipeline-box {
        background:white;
        border:1px solid #E5E7EB;
        border-radius:12px;
        padding:16px;
        min-width:140px;
        text-align:center;
        font-weight:600;
    }

    .pipeline-arrow {
        font-size:24px;
        color:#6B7280;
    }

    .summary-card {
        background:white;
        border:1px solid #E5E7EB;
        border-radius:12px;
        padding:16px;
        text-align:center;
    }

    .summary-label {
        color:#6B7280;
        font-size:0.85rem;
    }

    .summary-value {
        color:#111111;
        font-size:1.4rem;
        font-weight:700;
    }

    </style>
    """, unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

def render_sidebar():

    with st.sidebar:

        st.title("Simulation")

        input_text = st.text_area(
            "Input Message",
            value="Hello World",
            label_visibility="collapsed"
        )

        snr_db = st.slider(
            "Signal To Noise Ratio",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.5,
            label_visibility="collapsed"
        )

        run_clicked = st.button(
            "Run Simulation",
            use_container_width=True
        )

        st.divider()

        show_trellis = st.checkbox(
            "Show Trellis",
            value=True
        )

        show_ber = st.checkbox(
            "Show BER Analysis",
            value=True
        )

    return (
        input_text,
        snr_db,
        run_clicked,
        show_trellis,
        show_ber
    )


# ============================================================
# HEADER
# ============================================================

def render_header():

    st.title("Convolutional Encoder & Viterbi Decoder")

    st.caption(
        "Interactive demonstration of forward error correction using "
        "rate-1/2 convolutional coding and Viterbi decoding."
    )


# ============================================================
# PIPELINE
# ============================================================

def render_pipeline(stage):

    html = """
    <div class='pipeline-container'>
    """

    steps = [
        ("Text", stage["text"]),
        ("Binary", stage["binary"]),
        ("Encoder", stage["encoded"]),
        ("AWGN", f"{stage['snr']} dB"),
        ("Decoder", stage["decoded"]),
        ("Output", stage["recovered"])
    ]

    for i, (name, value) in enumerate(steps):

        html += f"""
        <div class='pipeline-box'>
            <div>{name}</div>
            <small>{value}</small>
        </div>
        """

        if i != len(steps)-1:
            html += "<div class='pipeline-arrow'>→</div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# SUMMARY
# ============================================================

def render_summary(
    original_text,
    recovered_text,
    ber,
    errors_corrected,
    snr_db
):

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class='summary-card'>
            <div class='summary-label'>Original</div>
            <div class='summary-value'>{original_text}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='summary-card'>
            <div class='summary-label'>Recovered</div>
            <div class='summary-value'>{recovered_text}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='summary-card'>
            <div class='summary-label'>BER</div>
            <div class='summary-value'>{ber:.6f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='summary-card'>
            <div class='summary-label'>Errors Corrected</div>
            <div class='summary-value'>{errors_corrected}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# BITSTREAM
# ============================================================

def render_bitstream(bits, title):

    grouped = " ".join(
        bits[i:i+8]
        for i in range(0, len(bits), 8)
    )

    st.subheader(title)

    st.code(
        grouped,
        language="text"
    )


# ============================================================
# TRELLIS
# ============================================================

def render_trellis(
    trellis_path,
    state_labels=["00","01","10","11"]
):

    if not trellis_path:
        st.info("No trellis path available.")
        return

    fig = go.Figure()

    path_x = []
    path_y = []

    for i, step in enumerate(trellis_path):

        path_x.extend([i, i+1, None])

        path_y.extend([
            step["from_state"],
            step["to_state"],
            None
        ])

    fig.add_trace(
        go.Scatter(
            x=path_x,
            y=path_y,
            mode="lines+markers",
            line=dict(width=3),
            marker=dict(size=10),
            name="Survivor Path"
        )
    )

    fig.update_layout(
        height=500,
        template="plotly_white",
        xaxis_title="Time Step",
        yaxis_title="State",
        yaxis=dict(
            tickvals=[0,1,2,3],
            ticktext=state_labels
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# BER PLOT
# ============================================================

def render_ber_plot(
    snr_values,
    ber_values,
    theoretical_ber=None
):

    fig, ax = plt.subplots(
        figsize=(8,4)
    )

    ax.semilogy(
        snr_values,
        ber_values,
        marker="o",
        label="Simulated"
    )

    if theoretical_ber is not None:

        ax.semilogy(
            snr_values,
            theoretical_ber,
            "--",
            label="Theoretical"
        )

    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel("BER")
    ax.grid(True)

    ax.legend()

    st.pyplot(fig)
