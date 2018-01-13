from binascii import hexlify

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
from gmpy2 import powmod

from .attacks import common_divisor, LSBOracle

import pytest
from hypothesis import given, reject, assume, settings
from hypothesis.strategies import integers, text, sampled_from

@pytest.fixture()
def key():
    return RSA.generate(1024)


@given(integers(), integers())
@settings(deadline=None)
@pytest.mark.slow
def test_common_divisor(key, x, plain):
    assume(0 < x < key.n)
    assume(0 < plain < key.n)
    sk = common_divisor(key.publickey(), key.p * x)
    cipher = powmod(plain, key.e, key.n)
    assert int(powmod(cipher, sk.d, sk.n)) == plain


@given(integers())
@settings(deadline=None)
@pytest.mark.slow
def test_lsb_oracle(key, plain):
    assume(0 < plain < key.n)

    class TestLSBOracle(LSBOracle):
        def query(self, m: int):
            return powmod(m, key.d, self.pk.n) % 2

    target = powmod(plain, key.e, key.n)
    o = TestLSBOracle(key.publickey(), target)
    assert o.run() == plain


