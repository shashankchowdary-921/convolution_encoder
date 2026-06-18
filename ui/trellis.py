import streamlit as st
import plotly.graph_objects as go


def render_trellis(trellis_path):

    if not trellis_path:
        st.info("No trellis path available")
        return

    fig = go.Figure()

    x = []
    y = []

    for i, step in enumerate(trellis_path):

        x.extend([
            i,
            i + 1,
            None
        ])

        y.extend([
            step["from_state"],
            step["to_state"],
            None
        ])

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            name="Path"
        )
    )

    fig.update_layout(
        title="Viterbi Trellis",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )
