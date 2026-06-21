class ConvolutionalEncoder:
    """Rate-1/2, K=3 convolutional encoder with G₁=111, G₂=101."""

    def __init__(self):
        self.reg = [0, 0, 0]          # shift register [x[n], x[n-1], x[n-2]]
        self.g1_taps = [0, 1, 2]      # 111
        self.g2_taps = [0, 2]         # 101

    def reset(self):
        self.reg = [0, 0, 0]

    def _shift(self, bit: int):
        self.reg[2] = self.reg[1]
        self.reg[1] = self.reg[0]
        self.reg[0] = bit

    def _compute_output(self, taps):
        result = 0
        for tap in taps:
            result ^= self.reg[tap]
        return result

    def encode(self, bits: str, terminate: bool = True) -> str:
        print("ENCODE CALLED, terminate =", terminate, "input len =", len(bits))
        """
        Encode a binary string, returns double-length codeword.
        If terminate=True, appends (K-1)=2 zero flush bits so the
        shift register returns to the all-zero state at the end,
        giving Viterbi a known terminal state to trace back from.
        """
        self.reset()
        if terminate:
            bits = bits + '0' * 2
        output = []
        for bit in bits:
            self._shift(int(bit))
            out1 = self._compute_output(self.g1_taps)
            out2 = self._compute_output(self.g2_taps)
            output.append(str(out1))
            output.append(str(out2))
        return ''.join(output)
