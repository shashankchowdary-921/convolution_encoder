import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def find_coding_gain(snr_values, ber_values, theoretical_ber):
    """
    Find the SNR gap between simulated and theoretical curves,
    measured at a BER level with genuine (non-floored) statistics —
    not at the floor edge, where a single bit error vs zero errors
    is the difference between two trial outcomes, not a stable estimate.
    """
    snr_values = np.array(snr_values)
    ber_values = np.array(ber_values)
    theoretical_ber = np.array(theoretical_ber)

    ber_floor = 1e-4
    # Require comfortably above the floor — real, resolved statistics
    valid = ber_values > ber_floor * 3

    if not np.any(valid):
        return None

    target_idx = np.where(valid)[0][-1]
    target_ber = ber_values[target_idx]
    sim_snr = snr_values[target_idx]

    theory_snr = np.interp(
        target_ber,
        theoretical_ber[::-1],
        snr_values[::-1]
    )

    gain_db = theory_snr - sim_snr
    return gain_db, target_ber, sim_snr, theory_snr


def render_ber_plot(
    snr_values,
    ber_values,
    theoretical_ber=None,
    num_trials=None,
    snr_step=None
):
    fig, ax = plt.subplots(
        figsize=(8, 4)
    )

    ber_floor = 1e-4
    ber_plot_values = [
        max(b, ber_floor) for b in ber_values
    ]

    ax.semilogy(
        snr_values,
        ber_plot_values,
        marker="o",
        label="Simulated"
    )

    if theoretical_ber is not None:
        ax.semilogy(
            snr_values,
            theoretical_ber,
            linestyle="--",
            label="Theoretical (Uncoded BPSK)"
        )

        gain_result = find_coding_gain(
            snr_values, ber_values, theoretical_ber
        )
        if gain_result is not None:
            gain_db, target_ber, sim_snr, theory_snr = gain_result
            ax.annotate(
                f"Coding gain ≈ {gain_db:.1f} dB\nat BER ≈ {target_ber:.0e}",
                xy=(sim_snr, target_ber),
                xytext=(sim_snr + 1.5, target_ber * 5),
                fontsize=9,
                arrowprops=dict(arrowstyle="->", color="#4F46E5"),
                color="#4F46E5",
                fontweight="bold"
            )

    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel("BER")
    ax.set_ylim(bottom=ber_floor / 2)
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)
    plt.close(fig)

    if num_trials is not None and snr_step is not None:
        st.caption(
            f"Methodology: each point averaged over {num_trials} independent "
            f"AWGN trials, SNR swept in {snr_step} dB steps. Codeword "
            f"terminated (K-1 flush bits) before transmission."
        )
