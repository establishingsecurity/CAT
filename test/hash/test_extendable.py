import struct
from binascii import hexlify
from ctypes import c_ulonglong

import pytest
from Cryptodome.Hash import SHA256, SHA512
from Cryptodome.Util.number import bytes_to_long
from hypothesis import assume, given
from hypothesis.strategies import binary, composite, lists

from cat.hash.extendable import *


@composite
def byte_array(draw):
    data = draw(lists(binary()))
    return b"".join(data)


@given(byte_array(), byte_array(), byte_array())
def test_length_extension_attack_sha256(secret, original_data, data_to_add):
    assume(len(original_data) > 0)
    assume(len(data_to_add) > 0)
    h = SHA256.new(secret + original_data).hexdigest()
    digest, message = hashpump(h, original_data, data_to_add, len(secret))
    assert message.startswith(original_data)
    assert message != original_data
    assert message.endswith(data_to_add)
    pad = message[len(original_data) : -len(data_to_add)]
    assert original_data + pad + data_to_add == message
    assert SHA256.new(secret + message).hexdigest() == digest


@given(byte_array(), byte_array(), byte_array())
def test_length_extension_attack_sha512(secret, original_data, data_to_add):
    assume(len(original_data) > 0)
    assume(len(data_to_add) > 0)
    h = SHA512.new(secret + original_data).hexdigest()
    digest, message = hashpump(h, original_data, data_to_add, len(secret))
    assert message.startswith(original_data)
    assert message != original_data
    assert message.endswith(data_to_add)
    pad = message[len(original_data) : -len(data_to_add)]
    assert original_data + pad + data_to_add == message
    assert SHA512.new(secret + message).hexdigest() == digest
