from Cryptodome.Hash import SHA512
from Cryptodome.Util.number import bytes_to_long
from ctypes import c_uint64

# TODO: extract common functions for all SHA objects into separate file

# SHA512 block size in bytes
block_size = 128

# SHA512 digest size in bytes
digest_size = 64

# SHA512 number of bytes for length of msg
l = 16

# SHA512 ctype
buffer_type = c_uint64

# SHA512 hash object
sha_type = SHA512

def load(load_state: bytes, input_length: int):
    r"""
    This function takes the digest of a Merkle–Damgård construction, the input
    length previously given to the hashfunction and returns the a copy of the
    original hash function

    >>> secret = b'TOTALLYSECURE'
    >>> h1 = SHA512.new(secret)
    >>> h2 = SHA512.new(pad(secret))
    >>> h3 = load(h1.digest(), len(secret))
    >>> h2.update(b'deadbeef')
    >>> h3.update(b'deadbeef')
    >>> h2.digest() == h3.digest()
    True
    """

    # calcuate the number of state entries in the buffer
    state_entry_bytes = 8

    # Preparing the load_state
    ls = data_to_buffer(load_state, 8, 8)

    # Creating the new hash object
    hash_object = sha_type.new()

    # Retrieving the state as array of c_uint64 objects
    state = get_state(hash_object, 11)

    # Changing the state (1st - 8th buffer entry)
    for (i, b) in enumerate(ls):
        state[i] = b

    # Changing the length of padded data at the 11th buffer entry
    data_length = 8 * get_data_length(input_length)
    state[10] = buffer_type(data_length)

    return hash_object


def data_to_buffer(load_state: bytes, no_of_entries: int, entry_size: int):
    r"""
    This function takes load_state, a byte array, and converts it to an array with number_of_entries entries of type buffer_type.
    """
    return [buffer_type(int.from_bytes(load_state[i:i+entry_size], 'big')) for i in range(0, digest_size, no_of_entries)]


def get_data_length(input_length: int):
    r"""
    This function returns the length of padded data in bytes for a given data length and block size in bytes.
    >>> get_data_length(111) == 128
    True
    >>> get_data_length(112) == 256
    True
    """

    return block_size * ((int((input_length + l) / block_size)) + 1)


def get_state(hash_object: sha_type, length: int):
    r"""
    This function takes a SHA512 object and the number of lines to retrieve from the buffer,
    returning the internal state as array of type c_uint64.
    The state of the SHA512 object consists of the following c_uint64 entries (8 bytes each):
    - S01
    - ...
    - S08
    - L
    - P01
    - ...
    - P16
    S ... internal state, L ... length of padded data in bit, P ... plaintext data for next round
    """
    state_pointer = hash_object._state.get()
    state_type = buffer_type * length
    return state_type.from_buffer(state_type.from_address(state_pointer.value))


# TODO maybe we should work with bits here, currently this function only supports full bytes as msg
def pad(payload: bytes):
    r"""
    This function takes a payload as byte array and the block size
    and returns the byte array plus the padding added before hashing it with SHA512.
	The padding consists of:
    - an '\x80' byte
    - k '0' bits, where k is the smallest non-negative solution to l + 1 + k = 112 mod 128
    - the length of the payload in bit using 16 bytes
    The length of the padded message is, therefore, a multiple of 64 byte

    >>> payload = b'A'*111
    >>> padded_payload = pad(payload)
    >>> len(padded_payload) % block_size == 0
    True
    >>> padded_payload == b'A'*111 + b'\x80' + b'\x00'*14 + b'\x03\x78'
    True
    """

    payload_length = len(payload)
    k = block_size - l - payload_length - 1
    while k < 0:
        k += block_size
    padding = b'\x80' + b'\x00'*k

    l_bit = 8 * payload_length
    length = l_bit.to_bytes(l, 'big')

    return payload + padding + length
