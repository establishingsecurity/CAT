from binascii import hexlify

from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.Util.number import getPrime
from gmpy2 import powmod, next_prime, mpz

from .attacks import *

import pytest
from hypothesis import given, reject, assume, settings
from hypothesis.strategies import integers, text, sampled_from

@pytest.fixture()
def key():
    return RSA.generate(1024)

@pytest.fixture()
def close_primes():
    p = getPrime(512)
    q = int(next_prime(p))
    return (p, q)

@pytest.fixture()
def plain_int():
    return 512

def test_fermat_factoring(close_primes, plain_int):
    p = close_primes[0]
    q = close_primes[1]
    plain = plain_int
    e = 2**16 + 1
    pk = RSA.construct((p*q, e))
    key = reconstruct_private(pk, p)

    sk = fermat_factoring(pk)

    cipher = powmod(plain, key.e, key.n)
    assert int(powmod(cipher, sk.d, sk.n)) == plain

@given(integers(), integers(min_value=1))
@settings(deadline=None)
@pytest.mark.slow
def test_common_divisor(key, x, plain):
    assume(0 < x < key.n)
    assume(0 < plain < key.n)
    sk = common_divisor(key.publickey(), key.p * x)
    cipher = powmod(plain, key.e, key.n)
    assert int(powmod(cipher, sk.d, sk.n)) == plain


def test_lsb_oracle_fix(key):
    plain = 0xdeadbeef
    assert plain < key.n

    d = mpz(key.d)
    n = mpz(key.n)

    def oracle(c):
        return powmod(c, d, n) % 2

    target = powmod(plain, key.e, key.n)
    assert plain == lsb_oracle(key.publickey(), target, oracle)

@given(integers(min_value=1))
@settings(deadline=None)
@pytest.mark.slow
def test_lsb_oracle(key, plain):
    assume(0 < plain < key.n)

    d = mpz(key.d)
    n = mpz(key.n)

    def oracle(c):
        return powmod(c, d, n) % 2

    target = powmod(plain, key.e, key.n)
    assert plain == lsb_oracle(key.publickey(), target, oracle)
