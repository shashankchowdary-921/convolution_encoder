class ViterbiDecoder:
    """Viterbi decoder for rate-1/2, K=3 convolutional code (4 states)."""
    
    def __init__(self):
        self.num_states = 4
        self.next_state = {}
        self.output = {}
        self._build_trellis()
    
    def _build_trellis(self):
        """Build trellis transitions for states 0-3 (00,01,10,11)."""
        for state in range(self.num_states):
            reg = [(state >> 1) & 1, state & 1]   # [x[n-1], x[n-2]]
            for input_bit in [0, 1]:
                full_reg = [input_bit, reg[0], reg[1]]
                out1 = full_reg[0] ^ full_reg[1] ^ full_reg[2]   # G1 = 111
                out2 = full_reg[0] ^ full_reg[2]                 # G2 = 101
                next_state = (input_bit << 1) | reg[0]
                self.next_state[(state, input_bit)] = next_state
                self.output[(state, input_bit)] = (out1, out2)
    
    def _hamming_distance(self, bits1, bits2):
        return (bits1[0] ^ bits2[0]) + (bits1[1] ^ bits2[1])
    
    def decode(self, received_bits: str) -> str:
        """Decode received bitstream (even length)."""
        if len(received_bits) % 2 != 0:
            raise ValueError("Received bits must have even length")
        
        received_pairs = [(int(received_bits[i]), int(received_bits[i+1])) 
                         for i in range(0, len(received_bits), 2)]
        
        path_metrics = [float('inf')] * self.num_states
        path_metrics[0] = 0
        survivors = []
        
        for received_pair in received_pairs:
            new_metrics = [float('inf')] * self.num_states
            survivors_step = {}
            for state in range(self.num_states):
                if path_metrics[state] == float('inf'):
                    continue
                for input_bit in [0, 1]:
                    next_state = self.next_state[(state, input_bit)]
                    output = self.output[(state, input_bit)]
                    branch_metric = self._hamming_distance(received_pair, output)
                    candidate_metric = path_metrics[state] + branch_metric
                    if candidate_metric < new_metrics[next_state]:
                        new_metrics[next_state] = candidate_metric
                        survivors_step[next_state] = (state, input_bit)
            path_metrics = new_metrics
            survivors.append(survivors_step)
        
        # Traceback
        best_state = min(range(self.num_states), key=lambda s: path_metrics[s])
        decoded_bits = []
        for step in range(len(survivors) - 1, -1, -1):
            prev_state, input_bit = survivors[step][best_state]
            decoded_bits.append(str(input_bit))
            best_state = prev_state
        
        decoded_bits.reverse()
        return ''.join(decoded_bits)
    
    def decode_with_trellis(self, received_bits: str) -> dict:
        """Decode and also return trellis path for visualization."""
        if len(received_bits) % 2 != 0:
            raise ValueError("Received bits must have even length")
        
        received_pairs = [(int(received_bits[i]), int(received_bits[i+1])) 
                         for i in range(0, len(received_bits), 2)]
        
        path_metrics = [float('inf')] * self.num_states
        path_metrics[0] = 0
        survivors = []
        
        for received_pair in received_pairs:
            new_metrics = [float('inf')] * self.num_states
            survivors_step = {}
            for state in range(self.num_states):
                if path_metrics[state] == float('inf'):
                    continue
                for input_bit in [0, 1]:
                    next_state = self.next_state[(state, input_bit)]
                    output = self.output[(state, input_bit)]
                    branch_metric = self._hamming_distance(received_pair, output)
                    candidate_metric = path_metrics[state] + branch_metric
                    if candidate_metric < new_metrics[next_state]:
                        new_metrics[next_state] = candidate_metric
                        survivors_step[next_state] = (state, input_bit)
            path_metrics = new_metrics
            survivors.append(survivors_step)
        
        best_state = min(range(self.num_states), key=lambda s: path_metrics[s])
        decoded_bits = []
        trellis_path = []
        current_state = best_state
        
        for step in range(len(survivors) - 1, -1, -1):
            prev_state, input_bit = survivors[step][current_state]
            trellis_path.append({
                'step': step,
                'from_state': prev_state,
                'to_state': current_state,
                'input_bit': input_bit
            })
            decoded_bits.append(str(input_bit))
            current_state = prev_state
        
        decoded_bits.reverse()
        trellis_path.reverse()
        
        return {
            'output': ''.join(decoded_bits),
            'trellis_path': trellis_path
        }
