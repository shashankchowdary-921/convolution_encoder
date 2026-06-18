
import streamlit as st
import plotly.graph_objects as go


def render_trellis(
    trellis_path,
    state_labels=["00", "01", "10", "11"]
):

    if not trellis_path:
        st.warning("No trellis path available.")
        return

    fig = go.Figure()

    x_vals = []
    y_vals = []

    for idx, step in enumerate(trellis_path):

        x_vals.extend([
            idx,
            idx + 1,
            None
        ])

        y_vals.extend([
            step["from_state"],
            step["to_state"],
            None
        ])

    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines+markers",
            name="Survivor Path"
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=550,
        title="Viterbi Survivor Path",
        xaxis_title="Time Step",
        yaxis_title="State",
        yaxis=dict(
            tickvals=[0, 1, 2, 3],
            ticktext=state_labels
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

