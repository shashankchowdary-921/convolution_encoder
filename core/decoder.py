class ViterbiDecoder:
    """
    Viterbi Decoder
    Rate = 1/2
    Constraint Length K = 3
    Generator Polynomials:
        G1 = 111
        G2 = 101
    """

    def __init__(self):
        self.num_states = 4
        self.next_state = {}
        self.output = {}
        self._build_trellis()

    def _build_trellis(self):
        """
        States:
            0 -> 00
            1 -> 01
            2 -> 10
            3 -> 11
        """

        for state in range(self.num_states):

            reg1 = (state >> 1) & 1
            reg2 = state & 1

            for input_bit in [0, 1]:

                full_reg = [input_bit, reg1, reg2]

                out1 = full_reg[0] ^ full_reg[1] ^ full_reg[2]
                out2 = full_reg[0] ^ full_reg[2]

                next_state = (input_bit << 1) | reg1

                self.next_state[(state, input_bit)] = next_state
                self.output[(state, input_bit)] = (out1, out2)

    def _hamming_distance(self, received, expected):

        return (
            (received[0] ^ expected[0]) +
            (received[1] ^ expected[1])
        )

    def decode(self, received_bits):

        if len(received_bits) % 2 != 0:
            raise ValueError(
                "Received bitstream length must be even."
            )

        received_pairs = []

        for i in range(0, len(received_bits), 2):

            received_pairs.append(
                (
                    int(received_bits[i]),
                    int(received_bits[i + 1])
                )
            )

        path_metrics = [float("inf")] * self.num_states
        path_metrics[0] = 0

        survivors = []

        for pair in received_pairs:

            new_metrics = [float("inf")] * self.num_states
            survivor_step = {}

            for state in range(self.num_states):

                if path_metrics[state] == float("inf"):
                    continue

                for input_bit in [0, 1]:

                    next_state = self.next_state[
                        (state, input_bit)
                    ]

                    expected_output = self.output[
                        (state, input_bit)
                    ]

                    branch_metric = self._hamming_distance(
                        pair,
                        expected_output
                    )

                    metric = (
                        path_metrics[state]
                        + branch_metric
                    )

                    if metric < new_metrics[next_state]:

                        new_metrics[next_state] = metric

                        survivor_step[next_state] = (
                            state,
                            input_bit
                        )

            path_metrics = new_metrics
            survivors.append(survivor_step)

        best_state = min(
            range(self.num_states),
            key=lambda s: path_metrics[s]
        )

        decoded_bits = []

        for step in range(
            len(survivors) - 1,
            -1,
            -1
        ):

            prev_state, input_bit = survivors[
                step
            ][best_state]

            decoded_bits.append(str(input_bit))

            best_state = prev_state

        decoded_bits.reverse()

        return "".join(decoded_bits)

    def decode_with_trellis(self, received_bits):

        if len(received_bits) % 2 != 0:
            raise ValueError(
                "Received bitstream length must be even."
            )

        received_pairs = []

        for i in range(0, len(received_bits), 2):

            received_pairs.append(
                (
                    int(received_bits[i]),
                    int(received_bits[i + 1])
                )
            )

        path_metrics = [float("inf")] * self.num_states
        path_metrics[0] = 0

        survivors = []

        for pair in received_pairs:

            new_metrics = [float("inf")] * self.num_states
            survivor_step = {}

            for state in range(self.num_states):

                if path_metrics[state] == float("inf"):
                    continue

                for input_bit in [0, 1]:

                    next_state = self.next_state[
                        (state, input_bit)
                    ]

                    expected_output = self.output[
                        (state, input_bit)
                    ]

                    branch_metric = self._hamming_distance(
                        pair,
                        expected_output
                    )

                    metric = (
                        path_metrics[state]
                        + branch_metric
                    )

                    if metric < new_metrics[next_state]:

                        new_metrics[next_state] = metric

                        survivor_step[next_state] = (
                            state,
                            input_bit
                        )

            path_metrics = new_metrics
            survivors.append(survivor_step)

        best_state = min(
            range(self.num_states),
            key=lambda s: path_metrics[s]
        )

        decoded_bits = []
        trellis_path = []

        current_state = best_state

        for step in range(
            len(survivors) - 1,
            -1,
            -1
        ):

            prev_state, input_bit = survivors[
                step
            ][current_state]

            trellis_path.append(
                {
                    "step": step,
                    "from_state": prev_state,
                    "to_state": current_state,
                    "input_bit": input_bit
                }
            )

            decoded_bits.append(
                str(input_bit)
            )

            current_state = prev_state

        decoded_bits.reverse()
        trellis_path.reverse()

        return {
            "output": "".join(decoded_bits),
            "trellis_path": trellis_path
        }
