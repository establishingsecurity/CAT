from hashpumpy import hashpump as _hashpump
from typing import Tuple


def hashpump(hexdigest, original_data, data_to_add, key_length):
    # type: (str, str, str, int) -> Tuple[str, str]
    """
    Extends the given hash with the given data and returns the extended hash.
    The function autodetects the type of hash used - it supports MD5, SHA1, SHA256 and SHA512.
    Uses the excellent `hashpumpy <https://github.com/bwall/HashPump>`_.

    :param hexdigest:
    :param original_data:
    :param data_to_add:
    :param key_length:
    :return: (digest, message)
    """
    return _hashpump(hexdigest, original_data, data_to_add, key_length)
