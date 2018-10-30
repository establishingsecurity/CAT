from binascii import unhexlify
from base64 import b64decode
from Cryptodome.Util.number import long_to_bytes

def hex_to_bytes(h):
    # type: str -> bytes
    """
    Converts a hex string to bytes
    """
    return unhexlify(h)

def base64_to_bytes(h):
    # type: str -> bytes
    """
    Converts a base64 string to bytes
    """
    return b64decode(h)

def int_to_bytes(i):
    # type: int -> bytes
    """
    Converts a long integer to bytes
    """
    return long_to_bytes(i)

