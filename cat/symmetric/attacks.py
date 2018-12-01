from bitstring import BitArray


def cbc_padding_oracle(iv, target, oracle):
    """
    The CBC Padding Oracle attack decrypts a target ciphertext with the help of
    an oracle that reports back whether the plaintext is padded correctly or
    not.
    """
    # TODO: This only works for full padding blocks
    plaintext = []
    block_length = len(iv)
    ciphertext = [iv] + target

    # Get the padding first
    plaintext_length = cbc_padding_oracle_length(iv, target, oracle)
    padding_block = BitArray(
        bytes=plaintext_length.to_bytes(1, byteorder="big") * plaintext_length
    )

    for iv_block, target_block in zip(ciphertext[:-2], ciphertext[1:-1]):
        plaintext_block = BitArray(int=0x0, length=block_length * 8)
        for i in range(1, block_length + 1):
            pos_bit = (i-1) * 8
            for guess in range(0, 256):
                pad_bytes = BitArray(
                    bytes=(
                        b"\x00" * (block_length - i)
                        + i.to_bytes(1, byteorder="big") * i
                    )
                )
                iv_bytes = BitArray(bytes=iv_block)
                guess_bytes = BitArray(int=guess, length=block_length * 8) << pos_bit
                iv_guess = iv_bytes ^ guess_bytes ^ pad_bytes ^ plaintext_block
                # import ipdb; ipdb.set_trace()
                if oracle(iv_guess.tobytes(), target_block):
                    plaintext_block.overwrite(BitArray(int=guess, length=8), (block_length*8) - (i*8))
                    break

        plaintext.append(plaintext_block.tobytes()[::-1])
    return plaintext


def cbc_padding_oracle_length(iv, target, oracle):
    """
    This is the length determination part of the CBC Padding Oracle attack.
    It returns the actual length of the plaintext
    """
    ciphertext_length = len(target) * len(iv)
    if len(target) >= 2:
        iv_bytes = BitArray(bytes=target[-2], length=len(iv) * 8)
    else:
        iv_bytes = BitArray(bytes=iv, length=len(iv) * 8)

    guess = BitArray(int=0x01, length=len(iv) * 8)

    # Slide the error term to the left byte by byte
    for p in range(1, 17):
        iv_guess = iv_bytes ^ (guess << (p * 8))
        if oracle(iv_guess.tobytes(), target[-1]):
            # Length is length of the ciphertext minus the length of the padding
            return ciphertext_length - p
    # If we did not find the length, it must be a whole block of padding
    return ciphertext_length - len(iv)
