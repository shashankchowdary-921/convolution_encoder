def text_to_bits(text: str) -> str:
    return ''.join(format(ord(char), '08b') for char in text)

def bits_to_text(bits: str) -> str:
    if len(bits) % 8 != 0:
        bits = bits + '0' * (8 - len(bits) % 8)
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def calculate_ber(original: str, recovered: str) -> float:
    max_len = max(len(original), len(recovered))
    orig_padded = original.ljust(max_len, '0')
    rec_padded = recovered.ljust(max_len, '0')
    errors = sum(1 for a, b in zip(orig_padded, rec_padded) if a != b)
    return errors / max_len
