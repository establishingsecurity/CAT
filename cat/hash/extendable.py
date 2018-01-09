from Cryptodome.Hash import SHA256
from ctypes import c_ubyte

def load(load_state: bytes, input_length: int):
    r"""
    This function takes the digest of a Merkle–Damgård construction, the length
    of the original output and a message to extend it with, and returns the a
    copy of the original hash function

    >>> h1 = SHA256.new(b'deadbeef')
    >>> h1.digest()
    b'+\xaf\x1f@\x10]\x95\x01\xfe1\x9a\x8e\xc4c\xfd\xf42Z*]\xf4E\xad\xf3\xf5r\xf6&%6x\xc9'
    >>> h2 = load(h1.digest(), len(b'deadbeef'))
    >>> h1.update(b'deadbeef')
    >>> h2.update(b'deadbeef')
    >>> h1.digest() == h2.digest()
    True
    """

    # Prepare the load_state
    # TODO: Do padding and stuff

    # Creating the new hash object
    hash_object = SHA256.new()

    # Retrieving the state as byte array
    state_pointer = hash_object._state.get()
    state_type = c_ubyte * 64
    state = state_type.from_address(state_pointer.value)

    # Changing the state
    for (i, b) in enumerate(state):
        state[i] = b

    return hash_object
