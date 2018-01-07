from binascii import unhexlify
from base64 import b64decode
from Cryptodome.Util.number import long_to_bytes

def hex_to_bytes(h: str) -> bytes:
    """
    Converts a hex string to bytes

    >>> hex_to_bytes('deadbeef')
    b'\xde\xad\xbe\xef'
    """
    return unhexlify(h)

def base64_to_bytes(h: str) -> bytes:
    """
    Converts a base64 string to bytes

    >>> base64_to_bytes('3q2+7w==')
    b'\xde\xad\xbe\xef'
    """
    return b64decode(h)

def int_to_bytes(i: int) -> bytes:
    """
    Converts a long integer to bytes

    >>> int_to_bytes(3735928559)
    b'\xde\xad\xbe\xef'
    """
    return long_to_bytes(i)

