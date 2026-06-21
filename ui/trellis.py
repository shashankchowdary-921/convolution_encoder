import streamlit as st
import plotly.graph_objects as go

STATE_LABELS = {
    0: "00",
    1: "01",
    2: "10",
    3: "11",
}

def render_trellis(trellis_path):
    if not trellis_path:
        st.info("No trellis path available")
        return

    x = []
    y = []
    for i, step in enumerate(trellis_path):
        x.extend([i, i + 1, None])
        y.extend([step["from_state"], step["to_state"], None])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            line=dict(color="#7c9cff", width=2),
            marker=dict(size=5, color="#7c9cff"),
            name="Decoded Path",
            hovertemplate="Step %{x}<br>State %{y}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[trellis_path[0]["from_state"]],
            mode="markers",
            marker=dict(size=12, color="#3ddc84", symbol="circle"),
            name="Start (00)",
            hoverinfo="skip",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[len(trellis_path)],
            y=[trellis_path[-1]["to_state"]],
            mode="markers",
            marker=dict(size=12, color="#ff6b6b", symbol="circle"),
            name="End",
            hoverinfo="skip",
        )
    )

    fig.update_layout(
        title="Viterbi Trellis — Survivor Path",
        template="plotly_white",
        height=420,
        margin=dict(l=60, r=30, t=60, b=50),
        xaxis_title="Time Step (received bit pair index)",
        yaxis_title="Encoder State",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hovermode="closest",
    )

    fig.update_yaxes(
        tickmode="array",
        tickvals=[0, 1, 2, 3],
        ticktext=[f"{v} ({STATE_LABELS[v]})" for v in range(4)],
        range=[-0.5, 3.5],
        gridcolor="#e8e8e8",
    )

    fig.update_xaxes(
        gridcolor="#f0f0f0",
        rangeslider_visible=len(trellis_path) > 60,
    )

    st.plotly_chart(fig, width="stretch")
