class ConvolutionalEncoder:
    """Rate-1/2, K=3 convolutional encoder with G1=111, G2=101."""

    def __init__(self):
        self.reg = [0, 0, 0]
        self.g1_taps = [0, 1, 2]
        self.g2_taps = [0, 2]

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

    def encode_punctured(self, bits: str, terminate: bool = True) -> str:
        """
        Rate 2/3 via puncturing pattern [1,1,1,0] applied to rate-1/2 output.
        Every 4 bits of rate-1/2 output, drop the 4th bit.
        Output rate: 3 bits per 2 input bits.
        """
        rate_half = self.encode(bits, terminate=terminate)
        output = []
        for i, bit in enumerate(rate_half):
            if (i % 4) != 3:
                output.append(bit)
        return ''.join(output)
