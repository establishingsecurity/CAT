from Cryptodome.Hash import SHA256
from Cryptodome.Util.number import bytes_to_long
from ctypes import c_ulonglong

def load(load_state: bytes, input_length: int):
    r"""
    This function takes the digest of a Merkle–Damgård construction, the input
    length previously given to the hashfunction and returns the a copy of the
    original hash function

    >>> h1 = SHA256.new(b'A'*64)
    >>> h2 = load(h1.digest(), 64)
    >>> h1.update(b'deadbeef')
    >>> h2.update(b'deadbeef')
    >>> h1.digest() == h2.digest()
    True
    """

    # Prepare the load_state
    ls = [c_ulonglong(int.from_bytes(load_state[i:i+8], 'big')) for i in range(0, 64, 8)]

    # Creating the new hash object
    hash_object = SHA256.new(b'\x00' * input_length)

    # Retrieving the state as byte array
    state_pointer = hash_object._state.get()
    state_type = c_ulonglong * 8
    state = state_type.from_buffer(state_type.from_address(state_pointer.value))

    # Changing the state
    for (i, b) in enumerate(ls):
        state[i] = b

    return hash_object
