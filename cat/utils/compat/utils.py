import sys
from binascii import hexlify


def hex_str(byte_str):
    return hexlify(byte_str).decode("utf-8")


def to_bytes(str_):
    """
    Convert a Python3 string to bytes.

    In Python2 strings are bytes, so we just return the input.
    """
    if sys.version_info.major < 3:
        return str_
    else:
        return str_.encode("utf-8")
