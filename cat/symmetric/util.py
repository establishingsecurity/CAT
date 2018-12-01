from bitstring import BitArray

def block_chunks(text, block_size):
    """
    Collects the blocks from a ciphertext or padded plaintext and returns a list of it
    :param iterable: ciphertext of padded plaintext
    :param block_size: block size of the corresponding block cipher
    :return: list of blocks
    """
    if len(text) % block_size != 0:
        return None
    for i in range(0, len(text), block_size):
        yield text[i:i+block_size]


def edit_cbc_block(pre, position, from_value, to_value):
    """
    Changes the value at the specified position to the given value in the target ciphertext block.
    :param pre: Preceding block the target block
    :param position: Position of the changed value
    :param from_value: Actual value at position
    :param to_value: Target value at position
    :return: Edited preceding block
    """
    block_size = len(pre)
    pre = BitArray(bytes=pre)
    from_value = BitArray(bytes=from_value)
    to_value = BitArray(bytes=to_value)

    delta = BitArray(length=block_size*8)
    delta.overwrite(from_value ^ to_value, position*8)

    return (pre ^ delta).tobytes()
