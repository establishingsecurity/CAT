from bitstring import BitArray

from cat.symmetric.util import *


def guess_cbc_byte(
    pre,
    target_block,
    oracle,
    byte_pos,
    rem_plaintext,
    alphabet=[b.to_bytes(1, byteorder="big") for b in range(0, 256)],
):
    """
    Guesses the byte at the specified position of the target block in the
    ciphertext if the more significant remaining bytes of the block are given.
    Collects the blocks from a ciphertext or padded plaintext and returns a list of it
    :param pre: Preceding block the target block
    :param target_block: target ciphertext block
    :param oracle: Padding oracle
    :param byte_pos: Position of the byte in the block
    :param rem_plaintext: More significant bytes of the plaintext block
    :param alphabet: Alphabet of bytes to guesss from
    :return: Correct byte of target block at byte_pos
    """
    block_size = len(pre)
    pre = BitArray(bytes=pre)

    assert len(rem_plaintext) == (block_size - byte_pos) - 1

    # Generate the padding
    padding_byte = (block_size - byte_pos).to_bytes(1, byteorder="big")
    padding = padding_byte * (block_size - byte_pos)

    padding = BitArray(bytes=b"\x00" * byte_pos + padding)
    assert len(padding) == block_size * 8

    rem_plaintext = BitArray(bytes=(b"\x00" * (byte_pos + 1)) + rem_plaintext)
    assert len(rem_plaintext) == block_size * 8

    for guess in alphabet:
        # Generate the guess
        guess_bytes = BitArray(length=block_size * 8)
        guess_bytes.overwrite(guess, byte_pos * 8)

        # TODO: Proof that this is sound or find a sound alternative
        # If we query for the last byte, we change the second to last byte to
        # fix a corner case
        if byte_pos == block_size - 1:
            guess_bytes.overwrite(b'\x01', (byte_pos-1)*8)

        if guess_bytes == padding:
            continue

        guess_pre = padding ^ rem_plaintext ^ guess_bytes ^ pre

        # Something doesn't work here
        if oracle(guess_pre.tobytes(), target_block):
            return guess

    # We have hit the condition of guess_bytes == padding_bytes here
    return padding_byte

def cbc_padding_oracle(iv, target, oracle):
    """
    The CBC Padding Oracle attack decrypts a target ciphertext with the help of
    an oracle that reports back whether the plaintext is padded correctly or
    not.
    :param iv: IV of the ciphertext
    :param target: Ciphertext blocks
    :param oracle: Padding oracle
    :return: Reconstructed full plaintext
    """
    block_size = len(iv)
    ciphertext = [iv] + target
    for iv_block, target_block in zip(ciphertext[:-1], ciphertext[1:]):
        plaintext_block = b""
        for byte_pos in range(block_size-1, -1, -1):
            plaintext_block = (
                guess_cbc_byte(
                    iv_block, target_block, oracle, byte_pos, plaintext_block
                )
                + plaintext_block
            )
        yield plaintext_block


def cbc_padding_oracle_length(iv, target, oracle):
    """
    This is the length determination part of the CBC Padding Oracle attack.
    It returns the actual length of the plaintext
    """
    block_size = len(iv)
    ciphertext_length = len(target) * len(iv)
    if len(target) >= 2:
        iv_bytes = target[-2]
    else:
        iv_bytes = iv

    # Slide the error term to the left byte by byte
    # We begin at position -2 because we expect at least one byte of padding in
    # the last block
    for p in range(2, block_size + 1):
        # Guess the length of the padding is p-1
        guess_iv = edit_cbc_block(iv_bytes, block_size - p, b"\x00", b"\xff")
        if oracle(guess_iv, target[-1]):
            # Length is length of the ciphertext minus the length of the padding
            return ciphertext_length - (p - 1)
    # If we did not find the length, it must be a whole block of padding
    return ciphertext_length - block_size
