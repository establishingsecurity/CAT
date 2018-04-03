from Cryptodome.Hash import SHA256
from Cryptodome.Util.number import bytes_to_long
from ctypes import c_ulonglong

# SHA256 block size in bytes
block_size = 64

# SHA256 digest size in bytes
digest_size = 32

def load(load_state, input_length):
    # type: bytes, int
    r"""
    This function takes the digest of a Merkle–Damgard construction, the input
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
    ls = [c_ulonglong(int.from_bytes(load_state_aligned[i:i+8], 'big')) for i in range(0, digest_size, 8)]

    # Creating the new hash object
    hash_object = SHA256.new()

    # Retrieving the state as array of c_ulonglongs
    state = get_state(hash_object, 6)

    # Changing the state
    for (i, b) in enumerate(ls):
        state[i] = b

    # Changing the length of padded data
    data_length = (int((input_length + 8) / block_size)) * 8 * block_size + 8 * block_size
    state[5] = c_ulonglong(data_length)

    return hash_object

#TODO is it possible to get the state as array of objects that are half as long as c_ulonglong?
# (This would avoid switching data in the load function as well)
def get_state(hash_object, length):
    # type: SHA256, int
    r"""
    This function takes a SHA256 object and the number of lines to retrieve from the buffer,
    returning the internal state as array of type c_ulonglong.
    The state of the SHA256 object consists of the following c_ulonglong entries (2 x 4 bytes each):
    - S02 S01
    - S04 S03
    - S06 S05
    - S08 S07
    - ??
    - P01 L
    - P03 P02
    - ...
    - P15 P14
    -     P16
	S ... internal state, L ... length of padded data in bit, P ... plaintext data for next round
    """
    state_pointer = hash_object._state.get()
    state_type = c_ulonglong * length
    return state_type.from_buffer(state_type.from_address(state_pointer.value))


# TODO maybe we should work with bits here, currently this function only supports full bytes as msg
def pad(payload):
    # type: bytes
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
    >>> len(padded_payload) % block_size == 0
    True
    >>> padded_payload == b'A'*55 + b'\x80' + b'\x00'*6 + b'\x01\xb8'
    True
    """

    l = len(payload)
    k = block_size - 8 - l - 1
    while k < 0:
        k += block_size
    padding = b'\x80' + b'\x00'*k

    l_bit = 8 * l
    length = l_bit.to_bytes(8, 'big')

    return payload + padding + length
