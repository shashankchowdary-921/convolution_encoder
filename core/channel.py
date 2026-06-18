import numpy as np

class AWGNChannel:
    """Simulates AWGN channel with BPSK modulation."""
    
    @staticmethod
    def bits_to_symbols(bits: str) -> np.ndarray:
        bits_array = np.array([int(b) for b in bits], dtype=np.float32)
        return 2 * bits_array - 1   # 0→-1, 1→+1
    
    @staticmethod
    def symbols_to_bits(symbols: np.ndarray) -> str:
        return ''.join('1' if s > 0 else '0' for s in symbols)
    
    @staticmethod
    def calculate_noise_variance(snr_db: float) -> float:
        snr_linear = 10 ** (snr_db / 10)
        return 1 / (2 * snr_linear)
    
    def transmit(self, bits: str, snr_db: float):
        """Transmit bits through AWGN channel, returns (received_bits, tx_symbols, rx_symbols)."""
        tx_symbols = self.bits_to_symbols(bits)
        noise_var = self.calculate_noise_variance(snr_db)
        noise = np.random.normal(0, np.sqrt(noise_var), tx_symbols.shape)
        rx_symbols = tx_symbols + noise
        rx_bits = self.symbols_to_bits(rx_symbols)
        return rx_bits, tx_symbols, rx_symbols
