from Cryptodome.Hash import SHA256
from Cryptodome.Util.number import bytes_to_long
from ctypes import c_ulonglong

def load(load_state: bytes, input_length: int):
    r"""
    This function takes the digest of a Merkle–Damgård construction, the input
    length previously given to the hashfunction and returns the a copy of the
    original hash function

    >>> secret = b'TOTALLYSECURE'
    >>> h1 = SHA256.new(secret)
    >>> h2 = SHA256.new(pad(secret))
    >>> h3 = load(h1.digest(), len(secret))
    >>> h2.update(b'deadbeef')
    >>> h3.update(b'deadbeef')
    >>> h2.digest() == h3.digest()
    True
    """

    # Swapping groups of four bytes
    load_state_grouped = list(zip(*[iter(load_state)] * 4))
    load_state_swapped = ([c for t in zip(load_state_grouped[1::2], load_state_grouped[::2]) for c in t])
    load_state_aligned = [i for s in load_state_swapped for i in s]

    # Preparing the load_state
    ls = [c_ulonglong(int.from_bytes(load_state_aligned[i:i+8], 'big')) for i in range(0, 32, 8)]

    # Creating the new hash object
    hash_object = SHA256.new()

    # Retrieving the state as byte array
    state_pointer = hash_object._state.get()
    state_type = c_ulonglong * 6
    state = state_type.from_buffer(state_type.from_address(state_pointer.value))

    # Changing the state
    for (i, b) in enumerate(ls):
        state[i] = b

    # Changing the length of padded data
    data_length = (int((input_length + 8) / 64)) * 512 + 512
    state[5] = c_ulonglong(data_length)

    return hash_object


# TODO maybe we should work with bits here, currently this function only supports full bytes as msg
def pad(payload: bytes):
    r"""
    This function takes a payload as byte array and returns the byte array
    plus the padding added before hashing it with SHA256.
	The padding consists of:
    - an '\x80' byte
    - k '0' bits, where k is the smallest non-negative solution to l + 1 + k = 56 mod 64
    - the length of the payload in bit using 8 bytes
    The length of the padded message is, therefore, a multiple of 64 byte

    >>> payload = b'A'*55
    >>> padded_payload = pad(payload)
    >>> len(padded_payload) % 64 == 0
    True
    >>> padded_payload == b'A'*55 + b'\x80' + b'\x00'*6 + b'\x01\xb8'
    True
    """

    l = len(payload)
    k = 64 - 8 - l - 1
    while k < 0:
        k += 64
    padding = b'\x80' + b'\x00'*k

    l_bit = l * 8
    length = l_bit.to_bytes(8, 'big')

    return payload + padding + length
