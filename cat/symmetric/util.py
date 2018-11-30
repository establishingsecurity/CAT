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
