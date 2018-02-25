from Cryptodome.Hash import SHA512
import struct

from .extendable_sha_512 import *

import pytest
from hypothesis import given
from hypothesis.strategies import binary, lists, composite

@composite
def byte_array(draw):
    data = draw(lists(binary()))
    return b''.join(data)

@given(byte_array(), byte_array())
def test_length_extension_attack_sha512(secret, extend):
    h1 = SHA512.new(secret)
    h2 = SHA512.new(pad(secret))
    h3 = load(h1.digest(), len(secret))
    h2.update(extend)
    h3.update(extend)
    assert h2.digest() == h3.digest()
