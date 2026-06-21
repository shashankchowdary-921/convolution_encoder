import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def find_coding_gain(snr_values, ber_values, theoretical_ber):
    snr_values = np.array(snr_values)
    ber_values = np.array(ber_values)
    theoretical_ber = np.array(theoretical_ber)

    ber_floor = 1e-4
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
    fig, ax = plt.subplots(figsize=(8, 4))

    ber_floor = 1e-4
    ber_plot_values = [max(b, ber_floor) for b in ber_values]

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

        gain_result = find_coding_gain(snr_values, ber_values, theoretical_ber)
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


def render_constellation_plot(
    tx_symbols: np.ndarray,
    rx_symbols: np.ndarray,
    snr_db: float
):
    fig, ax = plt.subplots(figsize=(3.2, 2.3))

    jitter = np.random.normal(0, 0.08, size=rx_symbols.shape)
    ax.scatter(
        rx_symbols, jitter,
        alpha=0.3, s=12, color="#94A3B8", label="Received (noisy)"
    )

    for val, label in [(-1, "0"), (1, "1")]:
        ax.scatter(
            val, 0,
            s=120, zorder=5,
            color="#4F46E5",
            edgecolors="white",
            linewidths=1.5
        )
        ax.annotate(
            f"Bit {label}\n({val:+d})",
            xy=(val, 0),
            xytext=(val, 0.15),
            ha="center", fontsize=9,
            color="#4F46E5", fontweight="bold"
        )

    ax.axvline(0, color="#E11D48", linestyle="--", linewidth=1.2, label="Decision boundary")

    ax.set_xlim(-3, 3)
    ax.set_ylim(-1, 1)
    ax.set_xlabel("In-phase (I)")
    ax.set_yticks([])
    ax.set_title(f"BPSK Constellation — SNR = {snr_db:.1f} dB", fontsize=11)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)
    st.caption(
        "Each dot is one received symbol after AWGN corruption. "
        "Vertical spread is jitter for visibility (BPSK has no quadrature component). "
        "Symbols crossing x = 0 become bit errors."
    )
