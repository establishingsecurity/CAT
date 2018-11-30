from bitstring import BitArray


def cbc_padding_oracle(iv, target, oracle):
    """
    The CBC Padding Oracle attack decrypts a target ciphertext with the help of an oracle that reports back whether the plaintext is padded correctly or not.
    """
    block_length = len(iv)
    for block_count, (iv_block, target_block) in enumerate(
        zip([iv] + ciphertext[:-1], ciphertext)
    ):
        plaintext_block = b""
        if block_count == 0:
            plaintext_length = cbc_padding_oracle_length(iv, target, oracle)

        for i in reversed(range(1, block_length + 1)):
            padder = BitArray(bytes=(i.to_bytes(1) * i), length=block_length)
            for guess in range(0, 256):
                iv_guess = (
                    BitArray(bytes=iv_block)
                    ^ (BitArray(int=guess, length=block_length) << i)
                    ^ padder
                )
                if oracle(iv_guess, target_block):
                    plaintext_block += guess
        plaintext_block = reversed(plaintext_block)
        yield plaintext_block


def cbc_padding_oracle_length(iv, target, oracle):
    """
    This is the length determination part of the CBC Padding Oracle attack.
    It returns the actual length of the plaintext
    """
    ciphertext_length = len(target) * len(iv)
    iv_bytes = BitArray(bytes=target[-2], length=len(iv) * 8)
    guess = BitArray(int=0x01, length=len(iv) * 8)

    # Slide the error term to the left byte by byte
    for p in range(1, 17):
        iv_guess = iv_bytes ^ (guess << (p * 8))
        if oracle(iv_guess.tobytes(), target[-1]):
            # Length is length of the ciphertext minus the length of the padding
            return ciphertext_length - p
    # If we did not find the length, it must be a whole block of padding
    return ciphertext_length - len(iv)
