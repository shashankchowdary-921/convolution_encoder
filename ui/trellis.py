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
            line=dict(color="#4F46E5", width=2),
            marker=dict(size=5, color="#4F46E5"),
            name="Decoded Path",
            hovertemplate="Step %{x}<br>State %{y}<extra></extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[trellis_path[0]["from_state"]],
            mode="markers",
            marker=dict(size=12, color="#16A34A", symbol="circle"),
            name="Start (00)",
            hoverinfo="skip",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[len(trellis_path)],
            y=[trellis_path[-1]["to_state"]],
            mode="markers",
            marker=dict(size=12, color="#DC2626", symbol="circle"),
            name="End",
            hoverinfo="skip",
        )
    )

    fig.update_layout(
        title=dict(
            text="Viterbi Trellis — Survivor Path",
            font=dict(color="#111111", size=18),
        ),
        height=420,
        margin=dict(l=70, r=30, t=60, b=60),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        xaxis=dict(
            title=dict(text="Time Step (received bit pair index)", font=dict(color="#374151", size=13)),
            tickfont=dict(color="#374151", size=11),
            gridcolor="#E5E3DD",
            linecolor="#9CA3AF",
            zerolinecolor="#9CA3AF",
            rangeslider=dict(visible=len(trellis_path) > 60, bgcolor="#F0EFEA", bordercolor="#E5E3DD"),
        ),
        yaxis=dict(
            title=dict(text="Encoder State", font=dict(color="#374151", size=13)),
            tickfont=dict(color="#374151", size=11),
            tickmode="array",
            tickvals=[0, 1, 2, 3],
            ticktext=[f"{v} ({STATE_LABELS[v]})" for v in range(4)],
            range=[-0.5, 3.5],
            gridcolor="#E5E3DD",
            linecolor="#9CA3AF",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1,
            font=dict(color="#374151", size=12),
        ),
        hovermode="closest",
    )

    st.plotly_chart(fig, width="stretch")
