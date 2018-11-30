from bitstring import BitArray

def cbc_padding_oracle(iv, target, oracle):
    """
    The CBC Padding Oracle attack decrypts a target ciphertext with the help of an oracle that reports back whether the plaintext is padded correctly or not.
    """
    plaintext_length = cbc_padding_oracle_length(iv, target, oracle)


def cbc_padding_oracle_length(iv, target, oracle):
    """
    This is the length determination part of the CBC Padding Oracle attack.
    It returns the actual length of the plaintext
    """
    ciphertext_length = (len(target) * len(iv))
    iv_bytes = BitArray(bytes=target[-2], length=len(iv)*8)
    guess = BitArray(int=0x01, length=len(iv)*8)

    # Slide the error term to the left byte by byte
    for p in range(1,17):
        iv_guess = iv_bytes ^ (guess << (p * 8))
        if oracle(iv_guess.tobytes(), target[-1]):
            # Length is length of the ciphertext minus the length of the padding
            return ciphertext_length - p
    # If we did not find the length, it must be a whole block of padding
    return ciphertext_length - len(iv)
