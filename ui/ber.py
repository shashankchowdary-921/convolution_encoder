
import streamlit as st
import matplotlib.pyplot as plt


def render_ber_plot(
    snr_values,
    ber_values,
    theoretical_ber=None
):

    fig, ax = plt.subplots(
        figsize=(8, 4)
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
            linestyle="--",
            label="Theoretical"
        )

    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel("BER")

    ax.grid(True)

    ax.legend()

    st.pyplot(fig)

    plt.close(fig)

